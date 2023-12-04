from pydantic import BaseModel

class FilterCreate(BaseModel):
    """Filter create schema."""
    id: str