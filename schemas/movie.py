from typing import Optional
from pydantic import BaseModel, Field


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=25)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(ge=1900, le=2021)
    rating: float = Field(ge=0.0, le=10.0)
    category: str = Field(min_length=5, max_length=15)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Mi Pelicula",
                    "overview": "Descripcion de la pelicula",
                    "year": 2020,
                    "rating": 9.9,
                    "category": "Acción"
                }
            ]
        }
    }
