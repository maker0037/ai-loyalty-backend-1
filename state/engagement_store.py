# state/engagement_store.py

from typing import Dict, List
from datetime import datetime

ENGAGEMENT_STORE: Dict[str, List[dict]] = {}


def record_engagement(campaign_id: str, event_type: str, value: float = 0.0):
    event = {
        "event_type": event_type,   # open | click | conversion
        "value": value,
        "timestamp": datetime.utcnow().isoformat(),
    }

    ENGAGEMENT_STORE.setdefault(campaign_id, []).append(event)


def get_engagements(campaign_id: str) -> List[dict]:
    return ENGAGEMENT_STORE.get(campaign_id, [])
