"""Analyzer routes for the API."""
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from app.dependencies import get_analyzer,get_ingestor
from app.core.ingestion import Ingestor
from app.schemas.analyzer import  AnalyzerResponse
from app.core.analyzer import Analyzer
from typing import Annotated
from app.core.config import logger


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
    ingestor: Ingestor = Depends(get_ingestor),
    analyzer: Analyzer = Depends(get_analyzer)
):
    """
    Endpoint to upload a file for analysis.
    """
    try:
        ingested_file,ext = ingestor.ingest(file)
        print(ingested_file,ext)
        analysis_result = None
        if ext == "img" :
            analysis_result = analyzer.analyze_image(ingested_file)
        elif ext == "imgs":
            analysis_result = []
            for img in ingested_file:
                analysis_result.append(analyzer.analyze_image(img))
        elif ext == "text":
            analysis_result = analyzer.analyze_text(ingested_file)
        elif ext == "df":
            analysis_result = analyzer.analyze_dataframe(ingested_file)
        elif ext == "json":
            analysis_result = analyzer.analyze_json(ingested_file)
        return AnalyzerResponse(analysis=analysis_result, message="Analysis completed successfully.")
    except Exception as e:
        logger.error(f"Error during file analysis: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")
