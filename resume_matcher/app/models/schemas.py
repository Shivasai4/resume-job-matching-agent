from pydantic import BaseModel
from typing import Optional

class MatchSingleResponse(BaseModel):
    score: float
    explanation: str
    resume_text: str   # optionally return extracted text for transparency