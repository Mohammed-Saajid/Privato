# =================================================================
# 1. Builder Stage: Install dependencies
# =================================================================
FROM python:3.11.0-slim as builder

# Install system dependencies required for OpenCV and other packages
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*


WORKDIR /app

# Install uv, the fast package manager
RUN pip install uv

# Copy only the dependency file first to leverage Docker layer caching
COPY pyproject.toml ./

COPY .env ./

# Install production dependencies directly into the system Python
RUN uv pip install --system .

# Handle development dependencies if the build argument is set
ARG DEV=false
RUN if [ "$DEV" = "true" ] ; then uv pip install --system ".[dev]" ; fi

# =================================================================
# 2. Final Stage: Create the production image
# =================================================================
FROM python:3.11.0-slim

# Install system dependencies required for OpenCV and other packages
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*


WORKDIR /app

# Create a non-root user for security
RUN useradd --create-home appuser

# Copy the installed packages and executables from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN chown -R appuser:appuser /usr/local/lib/python3.11/site-packages
RUN chown -R appuser:appuser /usr/local/bin


# Copy the application and ML model files
COPY --chown=appuser:appuser app ./app
COPY --chown=appuser:appuser ml ./ml

# Switch to the non-root user
USER appuser

# Set Python path so imports from /app work correctly
ENV PYTHONPATH=/app:/app/app

# Expose the port and define the command to run the application
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]