from typing import List, Sequence, Any

from pydantic import BaseModel, StrictStr, StrictFloat

class SearchResponseResult(BaseModel):
    link: StrictStr
    title: StrictStr

class SearchResponse(BaseModel):
    results: List[SearchResponseResult]

class EmbedResponse(BaseModel):
    embedding: List[StrictFloat]

class ScrapeResponse(BaseModel):
    text: StrictStr

class ChatResponse(BaseModel):
    text: StrictStr

class TraceResponse(BaseModel):
    text: StrictStr

class SummarizeResponse(BaseModel):
    text: StrictStr

class ErrorResponse(BaseModel):
    error: StrictStr

class ValidationErrorResponse(ErrorResponse):
    context: Sequence[Any]