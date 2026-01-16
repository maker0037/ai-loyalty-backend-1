# services/access_control.py

def can_launch_campaign(role: str) -> bool:
    return role in {"admin", "marketing_manager"}
