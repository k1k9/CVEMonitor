from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class AlertCreate(BaseModel):
    """Alert create schema."""
    id: str
    description: str
    created_at: datetime
    status: str
    score: str
    scoreText: str
    url: str
    updated_at: Optional[datetime] = None
    is_acked: bool = False
    user_id: Optional[str] = None
    notes: Optional[str] = None
    
    
class AlertUpdate(BaseModel):
    """Alert update schema."""
    description: Optional[str] = None
    updated_at: Optional[datetime] = None
    status: Optional[str] = None
    score: Optional[str] = "0"
    scoreText: Optional[str] = "None"
    is_acked: Optional[bool] = None
    user_id: Optional[str] = None
    url: Optional[str] = None
    notes: Optional[str] = None