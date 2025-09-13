"""Redactor routes for the API."""
from app.core.ingestion import Ingestor
from app.dependencies import  get_ingestor, get_redactor
from fastapi import UploadFile, File, Depends, APIRouter, HTTPException
from app.core.redactor import Redactor
from app.core.utils import save_img_to_buffer
from fastapi.responses import StreamingResponse, JSONResponse
from io import BytesIO
from typing import Annotated
from app.core.config import logger


router = APIRouter(
    prefix="/redactor",
    tags=["redactor"]
)

@router.post(
    path="/upload_file",
    tags = ["redactor"],
    summary="Upload a file for analysis and redaction",
    description="Upload a file (image, text, json, csv) for analysis and redaction of sensitive information."
)


def redact_file(
    file : Annotated[UploadFile, File(description="File to be analyzed and redacted.")],
    ingestor : Ingestor = Depends(get_ingestor),
    redactor : Redactor = Depends(get_redactor)
):
    """
    Endpoint to upload a file for analysis and redaction.
    """
    try:
        ingested_file, ext = ingestor.ingest(file=file)
        redacted_result = None
        if ext == "img":
            redacted_result = redactor.redact_image(ingested_file)
            buffer = save_img_to_buffer(redacted_result)
            return StreamingResponse(buffer, media_type="image/png")
        elif ext == "text":
            redacted_result = redactor.redact_text(ingested_file)
            return JSONResponse(content=redacted_result, status_code=200)
        elif ext == "imgs":
            pdf_bytes = redactor.redact_pdf(ingested_file)
            if not pdf_bytes:
                     return JSONResponse(content={"error": "Failed to create PDF"}, status_code=500)
            return StreamingResponse(BytesIO(pdf_bytes), media_type="application/pdf", 
                                     headers={"Content-Disposition": f"attachment; filename=redacted_output.pdf"})
        elif ext == "json":
            redacted_result = redactor.redact_json(ingested_file)
        elif ext == "df":
            redacted_result = redactor.redact_df(ingested_file)

    except Exception as e:
        logger.error(f"Error during file redaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))
