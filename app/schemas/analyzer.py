"""Schemas for analyzer responses."""
from pydantic import BaseModel
from typing import List, Optional, Union, Dict



class AnalysisResult(BaseModel):
    entity_type: str
    start: int
    end: int
    score: float
    analysis_explanation: Optional[str] = None
    recognition_metadata: Optional[Dict] = None
    left: Optional[int] = None
    top: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None


class AnalyzerResponse(BaseModel):
    analysis: Optional[Union[List[AnalysisResult], List[List[AnalysisResult]]]] 
    message: Optional[str] = None
    error: Optional[str] = None
    
    model_config = {
        "json_schema_extra": {
        "example": [{  
            "analysis": [
                {
                    "entity_type": "person",
                    "start": 0,
                    "end": 5,
                    "score": 0.99,
                    "analysis_explanation": "Detected a person",
                    "recognition_metadata": {
                        "image_id": "X_000.jpeg",
                        "timestamp": "2023-10-01T12:00:00Z"
                    },
                    "left": 100,
                    "top": 150,
                    "width": 50,
                    "height": 100
                }
            ],
            "message": "Analysis completed successfully",
            "error": None
        }]
    }
    }