"""Redactor routes for the API."""
from core.ingestion import Ingestor
from app.dependencies import  get_ingestor, get_redactor
from fastapi import UploadFile, File, Depends, APIRouter, HTTPException, Form
from core.redactor import Redactor
from core.utils import save_img_to_buffer
from fastapi.responses import StreamingResponse, JSONResponse
from io import BytesIO
from typing import Annotated
from core.config import logger, SUPPORTED_LANGUAGES


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
    redactor : Redactor = Depends(get_redactor),
    language: str = Form(default="en", description="Language for redaction")
):
    """
    Endpoint to upload a file for analysis and redaction.
    """
    if language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Language '{language}' is not supported. Supported languages are: {list(SUPPORTED_LANGUAGES)}")
    try:
        ingested_file, ext = ingestor.ingest(file=file)
        redacted_result = redactor.redact(ingested_file, data_type=ext, language=language, download=True)
        if ext == "img":
            buffer = save_img_to_buffer(redacted_result)
            return StreamingResponse(buffer, media_type="image/png")
        elif ext == "text":
            return JSONResponse(content=redacted_result, status_code=200)
        elif ext == "imgs":
            if not redacted_result:
                return HTTPException(detail={"error": "Failed to create PDF"}, status_code=500)
            return StreamingResponse(BytesIO(redacted_result), media_type="application/pdf",
                                     headers={"Content-Disposition": f"attachment; filename=redacted_output.pdf"})
        elif ext == "json":
            NotImplementedError("JSON redaction not implemented yet.")
        elif ext == "df":
            NotImplementedError("DataFrame redaction not implemented yet.")
    
    except Exception as e:
        logger.error(f"Error during file redaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))
