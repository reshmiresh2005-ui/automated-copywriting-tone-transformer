from typing import Literal

from pydantic import BaseModel, Field, field_validator


Platform = Literal["LinkedIn", "Instagram", "Email"]


class CopyRequest(BaseModel):
    product_name: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1, max_length=4000)
    platform: Platform
    tone: str = Field(min_length=1, max_length=80)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    model: str | None = None

    @field_validator("product_name", "description", "tone")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be empty.")
        return value


class GeneratedCopy(BaseModel):
    product_name: str
    platform: Platform
    tone: str
    content: str
    character_count: int
    within_target: bool
    model: str
    temperature: float
    top_p: float
