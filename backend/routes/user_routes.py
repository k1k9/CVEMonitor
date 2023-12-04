from schemas import user_schema
from fastapi import APIRouter, Depends
from controllers import user_controller
from services.auth_service import check_is_logged, check_is_admin


router = APIRouter()

@router.get("/users")
async def get_users(token: str = Depends(check_is_admin)):
    """Get all users."""
    users = await user_controller.get_users()
    return users

@router.get("/user/{username}")
async def get_user(username: str,token: str = Depends(check_is_admin)):
    """Get user by username."""
    user = await user_controller.get_user(username)
    return user

@router.post("/user")
async def create_user(user: user_schema.UserCreate, token: str = Depends(check_is_admin)):
    """Create a new user."""
    created_user = await user_controller.create_user(user)
    return created_user 

@router.delete("/user/{id}")
async def delete_user(id: int, token: str = Depends(check_is_admin)):
    """Delete user by username."""
    user = await user_controller.delete_user(id)
    return user


@router.put("/user/{username}")
async def update_user(username: str, user: user_schema.UserUpdate, token: str = Depends(check_is_logged)):
    """Update user by username."""
    user = await user_controller.update_user(username, user)
    return user
