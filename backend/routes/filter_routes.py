from fastapi import APIRouter, Depends
from schemas import filter_schema
from controllers import filter_controller
from services.auth_service import check_is_logged

router = APIRouter()

@router.get("/filters")
async def get_filters(token: str = Depends(check_is_logged)):
    """Get all filters."""
    filters = await filter_controller.get_filters()
    return filters


@router.post("/filter")
async def create_filter(filter: filter_schema.FilterCreate, token: str = Depends(check_is_logged)):
    """Create a new filter."""
    filter = await filter_controller.create_filter(filter)
    return filter


@router.delete("/filter/{filter_id}")
async def delete_filter(filter_id: str,token: str = Depends(check_is_logged)):
    """Delete filter by filter_id."""
    filter = await filter_controller.delete_filter(filter_id)
    return filter