from typing import List
from fastapi import HTTPException
from passlib.context import CryptContext
from schemas import user_schema
from database import SessionLocal
from models.user_model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user(username: str) -> user_schema.UserGet:
    """Return user by username."""
    db = SessionLocal()
    error = HTTPException(status_code=404, detail="User not found")
    try: 
        user = db.query(User).where(User.username == username).first()
        if not user: raise error
    except:raise error 
    finally: db.close()
    return user_schema.UserGet(username=user.username, permissions=user.permissions, created_at=user.created_at)


async def get_users() -> List[user_schema.UserGet]:
    """Return all users."""
    db = SessionLocal()
    try:
        users = db.query(User).all()
    except:
        raise HTTPException(status_code=404, detail="Users not found")
    finally: db.close()
    return [user_schema.UserGet(id=user.id, username=user.username, permissions=user.permissions, created_at=user.created_at, last_login=user.last_login) for user in users]


async def create_user(user: user_schema.UserCreate):
    """Create user"""
    hash_password = pwd_context.hash(user.password)
    db = SessionLocal()
    db_user = User(username=user.username, password=hash_password, permissions=user.permissions)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except:
        raise HTTPException(status_code=400, detail="User already exists")
    finally: db.close()
    return {"message": "User created!", "code": 201}


async def delete_user(id: int):
    """Delete user by id."""
    db = SessionLocal()
    try:
        db.query(User).filter(User.id == id).delete()
        db.commit()
    except:
        raise HTTPException(status_code=404, detail="User not found")
    finally: db.close()
    return {"message": "User deleted", "code": 200}


async def update_user(username: str, user: user_schema.UserUpdate) -> user_schema.UserGet:
    """Update user by username."""
    db = SessionLocal()
    try:
        db = SessionLocal()
        db_user = db.query(User).filter(User.username == username).first()
        db_user.username = user.username if user.username else db_user.username
        db_user.password = user.password if user.password else db_user.password
        db_user.updated_at = user.updated_at if user.updated_at else db_user.updated_at
        db_user.permissions = user.permissions if user.permissions else db_user.permissions
        db.commit()
        db.refresh(db_user)
    except:
        raise HTTPException(status_code=404, detail="User not found")
    finally: db.close()
    return {"message": "User updated", "code": 200}




