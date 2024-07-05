from typing import Optional, List, Annotated

from pydantic import BaseModel, StrictStr, field_validator

from pydantic.types import StringConstraints

class RequestWithPrivateKey(BaseModel):
    private_key: Optional[Annotated[str, StringConstraints(strict=True, max_length=500)]] = None

    @field_validator('private_key')
    @classmethod
    def private_key_validation(cls, value: str) -> str:
        if value is not None and not value.strip():
            raise ValueError('must be non-empty and non-whitespace')

        return value

class ChatRequestMessage(BaseModel):
    role: StrictStr
    content: StrictStr

    @field_validator('role')
    @classmethod
    def role_validation(cls, value: StrictStr) -> StrictStr:
        if not value.strip():
            raise ValueError('must be non-empty and non-whitespace')

        return value

    @field_validator('content')
    @classmethod
    def content_validation(cls, value: StrictStr) -> StrictStr:
        if not value.strip():
            raise ValueError('must be non-empty and non-whitespace')

        return value

class ChatRequest(RequestWithPrivateKey):
    model: StrictStr
    messages: List[ChatRequestMessage]

    @field_validator('model')
    @classmethod
    def model_validation(cls, value: StrictStr) -> StrictStr:
        if not value.strip():
            raise ValueError('must be non-empty and non-whitespace')

        return value

    @field_validator('messages')
    @classmethod
    def messages_validation(cls, value: List[ChatRequestMessage]) -> List[ChatRequestMessage]:
        if not value:
            raise ValueError('must be non-empty')

        return value

    class Config:
        extra = "forbid"

        json_schema_extra = {
            "example": {
                "model": "gpt-4o",
                "messages": [
                    { "role": "user", "content": "Tell me a joke." }
                ]
            }
        }

class EmbedRequest(RequestWithPrivateKey):
    model: StrictStr
    input: StrictStr

    @field_validator('model')
    @classmethod
    def model_validation(cls, value: StrictStr) -> StrictStr:
        if not value.strip():
            raise ValueError('must be non-empty and non-whitespace')

        return value

    @field_validator('input')
    @classmethod
    def input_validation(cls, value: StrictStr) -> StrictStr:
        if not value.strip():
            raise ValueError('must be non-empty and non-whitespace')

        return value

    class Config:
        extra = "forbid"

        json_schema_extra = {
            "example": {
                "model": "text-embedding-3-small",
                "input": "The cat sat on the mat."
            }
        }

class SearchRequest(RequestWithPrivateKey):
    query: StrictStr

    @field_validator('query')
    @classmethod
    def query_validation(cls, value: StrictStr) -> StrictStr:
        if not value.strip():
            raise ValueError('must be non-empty and non-whitespace')

        return value

    class Config:
        extra = "forbid"

        json_schema_extra = {
            "example": {
                "query": "Best Italian restaurants in New York."
            }
        }

class ScrapeRequest(RequestWithPrivateKey):
    url: StrictStr

    @field_validator('url')
    @classmethod
    def url_validation(cls, value: StrictStr) -> StrictStr:
        if not value.strip():
            raise ValueError('must be non-empty and non-whitespace')

        return value

    class Config:
        extra = "forbid"

        json_schema_extra = {
            "example": {
                "url": "https://www.medoid.ai/blog/ai-economies-should-include-and-credit-content-creators-givebackgpt"
            }
        }

class CreditRequestResult(BaseModel):
    author: StrictStr
    link: StrictStr
    similarity_score: StrictStr

    @field_validator('author')
    @classmethod
    def author_validation(cls, value: StrictStr) -> StrictStr:
        if not value.strip():
            raise ValueError('must be non-empty and non-whitespace')

        return value

    @field_validator('link')
    @classmethod
    def link_validation(cls, value: StrictStr) -> StrictStr:
        if not value.strip():
            raise ValueError('must be non-empty and non-whitespace')

        return value

    @field_validator('similarity_score')
    @classmethod
    def similarity_score_validation(cls, value: StrictStr) -> StrictStr:
        if not value.strip():
            raise ValueError('must be non-empty and non-whitespace')

        try:
            float(value)
        except ValueError:
            raise ValueError('must be a string representing a valid float')

        return value

class CreditRequest(BaseModel):
    results: List[CreditRequestResult]

    @field_validator('results')
    @classmethod
    def results_validation(cls, value: List[CreditRequestResult]) -> List[CreditRequestResult]:
        if not value:
            raise ValueError('must be non-empty')

        return value

    class Config:
        extra = "forbid"

        json_schema_extra = {
            "example": {
                "results": [
                    { "author": "Anestis Fachantidis", "link": "https://www.medoid.ai/blog/ai-economies-should-include-and-credit-content-creators-givebackgpt", "similarity_score": "0.78" }
                ]
            }
        }

class SummarizeRequest(RequestWithPrivateKey):
    model: StrictStr
    input: StrictStr

    @field_validator('model')
    @classmethod
    def model_validation(cls, value: StrictStr) -> StrictStr:
        if not value.strip():
            raise ValueError('must be non-empty and non-whitespace')

        return value

    @field_validator('input')
    @classmethod
    def input_validation(cls, value: StrictStr) -> StrictStr:
        if not value.strip():
            raise ValueError('must be non-empty and non-whitespace')

        return value

    class Config:
        extra = "forbid"

        json_schema_extra = {
            "example": {
                "model": "gpt-4o",
                "input": "Despite facing numerous obstacles including financial difficulties, lack of institutional support, and widespread skepticism, the young entrepreneur managed to launch her innovative startup, which eventually revolutionized the renewable energy sector."
            }
        }

class TraceRequest(RequestWithPrivateKey):
    model: StrictStr
    input: StrictStr

    @field_validator('model')
    @classmethod
    def model_validation(cls, value: StrictStr) -> StrictStr:
        if not value.strip():
            raise ValueError('must be non-empty and non-whitespace')

        return value

    @field_validator('input')
    @classmethod
    def input_validation(cls, value: StrictStr) -> StrictStr:
        if not value.strip():
            raise ValueError('must be non-empty and non-whitespace')

        return value

    class Config:
        extra = "forbid"

        json_schema_extra = {
            "example": {
                "model": "gpt-4o",
                "input": "When I first started my fitness journey, I, Emily Carter, was overwhelmed by all the conflicting advice out there. Some people swore by intense workouts, while others advocated for slow and steady progress. It wasn’t until I found a routine that fit my lifestyle that I started seeing real results."
            }
        }