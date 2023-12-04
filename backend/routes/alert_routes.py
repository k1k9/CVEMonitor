from schemas import alert_schema
from services import nvd_service
from fastapi import APIRouter, Depends
from controllers import alert_controller
from services.auth_service import check_is_logged, check_is_admin

router = APIRouter()


@router.get("/stats/alerts")
async def get_alerts_stats(token: str = Depends(check_is_logged)):
    """Get specific statiscs about alerts."""
    stats = await alert_controller.get_alerts_stats()
    return stats


@router.get("/alerts/{offset}")
async def get_alerts(offset: int):
    """Get 10 latest alerts."""
    alerts = await alert_controller.get_alerts(offset)
    return alerts


@router.get("/alert/{alert_id}")
async def get_alert(alert_id: int, token: str = Depends(check_is_logged)):
    """Get alert by alert_id."""
    alert = await alert_controller.get_alert(alert_id)
    return alert


@router.delete("/alert/{alert_id}")
async def delete_alert(alert_id: int, token: str = Depends(check_is_admin)):
    """Delete alert by alert_id."""
    alert = await alert_controller.delete_alert(alert_id)
    return alert


@router.put("/alert/{alert_id}")
async def update_alert(alert_id: int, alert: alert_schema.AlertUpdate, token: str = Depends(check_is_admin)):
    """Update alert by alert_id."""
    alert = await alert_controller.update_alert(alert_id, alert)
    return alert


@router.get("/alert/{alert_id}/ack")
async def ack_alert(alert_id: str, token: str = Depends(check_is_logged)):
    """Acknowledge alert by alert_id."""
    alert = await alert_controller.ack_alert(alert_id)
    return alert


@router.get("/refresh")
async def refresh_alerts(token: str = Depends(check_is_logged)):
    """Refresh alerts."""
    alerts = await nvd_service.fetch_alerts()
    return alerts