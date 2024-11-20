from pydantic import BaseModel
from typing import List, Tuple, Any

class MatchRequest(BaseModel):
    source: List[Tuple[str, str]]
    target: List[Tuple[str, str]]

class MatchResponse(BaseModel):
    matches: List[Tuple[str, str, str, str, float]]
