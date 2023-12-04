import nvdlib
import datetime
from schemas import alert_schema
from controllers import alert_controller, filter_controller


async def fetch_alerts():
    """Fetch alerts from NVD."""
    filters = await filter_controller.get_filters()
    pubEndDate = datetime.datetime.now()
    pubStartDate = pubEndDate - datetime.timedelta(days=3)
    request = nvdlib.searchCVE(pubStartDate=pubStartDate, pubEndDate=pubEndDate)
    
    for alert in request:
        for _filter in filters:
            if _filter.id.lower() in alert.descriptions[0].value.lower():
                try:
                    await alert_controller.create_alert(alert_schema.AlertCreate(
                    id=alert.id,
                    created_at=alert.published,
                    description=alert.descriptions[0].value,
                    status = alert.vulnStatus,
                    score=str(alert.score[1]) if alert.score[1] is not None else "0",
                    scoreText=alert.score[2] if alert.score[2] is not None else "None",
                    url = alert.url,))
                except Exception as e: pass
    return {"message": "Alerts refreshed", "count": len(request)}