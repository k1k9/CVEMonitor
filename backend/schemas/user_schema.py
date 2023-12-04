from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class UserCreate(BaseModel):
    """User create schema."""
    username: str
    password: str
    permissions: int = 0
        
        
class UserUpdate(BaseModel):
    """User update schema."""
    username: Optional[str] = None
    password: Optional[str] = None
    updated_at: Optional[datetime] = None
    permissions: Optional[int] = None
    
    
class UserGet(BaseModel):
    """User get schema."""
    id: int
    username: str
    permissions: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    
class UserAuthenticate(BaseModel):
    """User authenticate schema."""
    username: str
    password: str