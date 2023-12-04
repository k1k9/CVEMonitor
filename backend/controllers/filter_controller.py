from schemas import filter_schema
from database import SessionLocal
from fastapi import HTTPException
from models.filter_model import Filter


async def get_filters():
    """Return all filters."""
    db = SessionLocal()
    filters = db.query(Filter).all()
    db.close()
    return filters


async def create_filter(filter: filter_schema.FilterCreate):
    """Create filter"""
    db = SessionLocal()
    try:
        db_filter = Filter(
            id=filter.id.lower().strip())
        db.add(db_filter)
        db.commit()
        db.refresh(db_filter)
    except:
        raise HTTPException(status_code=400, detail="Filter already exists")
    finally: db.close()
    return db_filter


async def delete_filter(filter_id: str):
    """Delete filter by filter_id."""
    db = SessionLocal()
    try:
        db.query(Filter).filter(Filter.id == filter_id).delete()
        db.commit()
    except:
        raise HTTPException(status_code=404, detail="Filter not found")
    finally: db.close()
    return {"message": "Filter deleted"}