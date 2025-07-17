# models.py
from pydantic import BaseModel
from typing import List

# Request model
class SearchRequest(BaseModel):
    url: str
    query: str

# Response result chunk model
class ChunkResult(BaseModel):
    text: str
    score: float  # semantic relevance score

# Full response model
class SearchResponse(BaseModel):
    results: List[ChunkResult]
