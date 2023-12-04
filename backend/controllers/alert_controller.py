from schemas import alert_schema
from database import SessionLocal
from fastapi import HTTPException
from models.alert_model import Alert


async def get_alerts(offset: int):
    """Get 10 latest alerts."""
    db = SessionLocal()
    try:
        alerts = db.query(Alert).order_by(Alert.created_at.desc()).offset(offset).limit(10).all()
    except:
        raise HTTPException(status_code=404, detail="Alerts not found")
    finally: db.close()
    return alerts


async def get_alerts_stats():
    """Get specific statiscs about alerts."""
    db = SessionLocal()
    try:
        alerts = db.query(Alert).all()
        total = len(alerts)
        critical = len([alert for alert in alerts if alert.scoreText == "CRITICAL"])
        high = len([alert for alert in alerts if alert.scoreText == "HIGH"])
        medium = len([alert for alert in alerts if alert.scoreText == "MEDIUM"])
        low = len([alert for alert in alerts if alert.scoreText == "LOW"])
        unknown = len([alert for alert in alerts if alert.scoreText == "None"])

        response = {
            "critical": critical, "high": high,
            "medium": medium, "low": low,
            "unknown": unknown, "total": total
        }
        return response
    except:
        raise HTTPException(status_code=404, detail="Alerts not found")
    finally: db.close()


async def get_alert(alert_id: int):
    """Get alert by alert_id."""
    db = SessionLocal()
    try:
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
    except:
        raise HTTPException(status_code=404, detail="Alert not found")
    finally: db.close()
    return alert


async def create_alert(alert: alert_schema.AlertCreate):
    """Create alert."""
    db = SessionLocal()
    try:
        db_alert = Alert(
            id=alert.id,
            description=alert.description,
            created_at=alert.created_at,
            updated_at=alert.updated_at,
            status=alert.status,
            score=alert.score,
            scoreText=alert.scoreText,
            is_acked=alert.is_acked,
            url=alert.url,
            notes=alert.notes)
        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)
    except:
        raise HTTPException(status_code=400, detail="Alert already exists")
    finally: db.close()
    return db_alert


async def delete_alert(alert_id: int):
    """Delete alert by alert_id."""
    db = SessionLocal()
    try:
        db.query(Alert).filter(Alert.id == alert_id).delete()
        db.commit()
    except:
        raise HTTPException(status_code=404, detail="Alert not found")
    finally: db.close()
    return {"message": "Alert deleted"}


async def update_alert(alert_id: int, alert: alert_schema.AlertUpdate):
    """Update alert by alert_id."""
    db = SessionLocal()
    try:
        db_alert = db.query(Alert).filter(Alert.id == alert_id).first()
        db_alert.description = alert.description if alert.description else db_alert.description
        db_alert.updated_at = alert.updated_at if alert.updated_at else db_alert.updated_at
        db_alert.status = alert.status if alert.status else db_alert.status
        db_alert.score = alert.score if alert.score else db_alert.score
        db_alert.scoreText = alert.scoreText if alert.scoreText else db_alert.scoreText
        db_alert.is_acked = alert.is_acked if alert.is_acked else db_alert.is_acked
        db_alert.acked_by = alert.acked_by if alert.acked_by else db_alert.acked_by
        db_alert.url = alert.url if alert.url else db_alert.url
        db_alert.notes = alert.notes if alert.notes else db_alert.notes
        db.commit()
        db.refresh(db_alert)
    except:
        raise HTTPException(status_code=404, detail="Alert not found")
    finally: db.close()
    return db_alert


async def ack_alert(alert_id: str):
    """Acknowledge alert by alert_id."""
    db = SessionLocal()
    try:
        db_alert = db.query(Alert).filter(Alert.id == alert_id).first()
        db_alert.is_acked = not db_alert.is_acked
        db.commit()
        db.refresh(db_alert)
    except:
        raise HTTPException(status_code=404, detail="Alert not found")
    finally: db.close()
    return db_alert

