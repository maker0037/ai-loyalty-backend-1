# services/execution_service.py

def execute_campaign(campaign: dict):
    """
    Dispatch campaign to external systems.
    (Email, SMS, Push, Webhook, etc.)
    """

    channel = campaign["channel"]

    if channel == "email":
        return {"status": "queued", "provider": "email_stub"}

    if channel == "sms":
        return {"status": "queued", "provider": "sms_stub"}

    if channel == "push":
        return {"status": "queued", "provider": "push_stub"}

    return {"status": "skipped"}
