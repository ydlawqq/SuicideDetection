from pydantic import BaseModel, Field
from typing import Annotated


class PredictRequest(BaseModel):
    texts: list[Annotated[str, Field(min_length=1, max_length=1024)]] = Field(
        min_length=1, max_length=32
    )


class PredictResponse(BaseModel):
    scores: list[float] = Field(
        min_length=1, max_length=32
    )

    