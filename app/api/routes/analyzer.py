"""Analyzer routes for the API."""
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status, Form
from app.dependencies import get_analyzer,get_ingestor
from core.ingestion import Ingestor
from app.schemas.analyzer import  AnalyzerResponse
from core.analyzer import Analyzer
from typing import Annotated
from core.config import logger,SUPPORTED_LANGUAGES


router = APIRouter(
    prefix="/analyzer",
    tags=["analyzer"]
)

@router.post(
    path="/upload_file",
    summary="Upload a file for analysis",
    description="Upload a file (image, text, json, csv) for analysis of sensitive information.",
    response_model=AnalyzerResponse,
)
def analyze_file(
    file: Annotated[UploadFile, File(description="File to be analyzed.")],
    language: Annotated[str, Form(description="Language of the content, e.g., 'en' for English.")] = "en",
    ingestor: Ingestor = Depends(get_ingestor),
    analyzer: Analyzer = Depends(get_analyzer)
):
    """
    Endpoint to upload a file for analysis.
    """
    if language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Language '{language}' is not supported. Supported languages are: {list(SUPPORTED_LANGUAGES)}"
        )

    try:
        ingested_file, ext = ingestor.ingest(file)
        analysis_result = analyzer.analyze(ingested_file, data_type=ext, language=language)    
        return AnalyzerResponse(analysis=analysis_result, message="Analysis completed successfully.")
    
    except Exception as e:
        logger.error(f"Error during file analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during file analysis."
        )
