from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class MovieCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=30)
    year: int = Field(..., ge=1888, le=2100)
    rating: float = Field(default=0.0, ge=0, le=10)
    description: str
    duration_limites: int
    genre: str
    director: str


class MovieResponse(BaseModel):
    id: int
    is_active: bool
    name: str
    year: int
    rating: float
    description: str
    duration_limites: int
    genre: str
    director: str

    model_config = ConfigDict(from_attributes=True)