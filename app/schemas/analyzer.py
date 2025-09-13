"""Schemas for analyzer responses."""
from pydantic import BaseModel
from typing import List, Optional, Union, Dict

class AnalyzerResponse(BaseModel):
    analysis: Union[List[List[Dict]],List[Dict],None] = None
    message: Optional[str] = None
    error: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True
    