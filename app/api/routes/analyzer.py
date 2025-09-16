"""Analyzer routes for the API."""
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status, Form
from app.dependencies import get_analyzer,get_ingestor
from app.core.ingestion import Ingestor
from app.schemas.analyzer import  AnalyzerResponse
from app.core.analyzer import Analyzer
from typing import Annotated
from app.core.config import logger,SUPPORTED_LANGUAGES


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
    language: Annotated[str,Form(description="Language of the content, e.g., 'en' for English.")] = "en",
    ingestor: Ingestor = Depends(get_ingestor),
    analyzer: Analyzer = Depends(get_analyzer)
):
    """
    Endpoint to upload a file for analysis.
    """
    try:
        if language not in SUPPORTED_LANGUAGES:
            raise ValueError("Language Not Supported")
        ingested_file,ext = ingestor.ingest(file)
        analysis_result = None
        if ext == "img" :
            analysis_result = analyzer.analyze_image(ingested_file,language=language)
        elif ext == "imgs":
            analysis_result = []
            for img in ingested_file:
                analysis_result.append(analyzer.analyze_image(img,language=language))
        elif ext == "text":
            analysis_result = analyzer.analyze_text(ingested_file,language=language)
        elif ext == "df":
            analysis_result = analyzer.analyze_dataframe(ingested_file,language=language)
        elif ext == "json":
            analysis_result = analyzer.analyze_json(ingested_file,language=language)
        return AnalyzerResponse(analysis=analysis_result, message="Analysis completed successfully.")
    except Exception as e:
        logger.error(f"Error during file analysis: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")
