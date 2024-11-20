from fastapi import APIRouter, HTTPException
from app.models.fuzzy_matcher_model import MatchRequest, MatchResponse
from app.services.fuzzy_matcher import perform_fuzzy_match

router = APIRouter()

@router.post("/vsky_fuzzy_match", response_model=MatchResponse)
def fuzzy_match(data: MatchRequest):
    if not data.source or not data.target:
        raise HTTPException(status_code=400, detail="Source and target lists cannot be empty.")
    
    matches = perform_fuzzy_match(data.source, data.target)
    return MatchResponse(matches=matches)
