# services/campaign_service.py

from datetime import datetime
from uuid import uuid4

from agents.orchestrator import generate_campaign_recommendations
from agents.message_agent import generate_campaign_messages
from agents.autonomy_agent import should_auto_launch

from services.metrics_service import refresh_campaign_metrics
from services.execution_service import execute_campaign

from state.audit_log_store import log_event
from state.campaign_store import (
    save_campaign,
    get_campaign,
    get_all_campaigns,
)
from state.learning_store import get_learning


# -------------------------------------------------
# 1️⃣ CAMPAIGN PREVIEW (NO STORAGE)
# -------------------------------------------------
def preview_campaign(segment_id: str) -> dict:
    """
    Build a UI-ready preview for Review & Launch modal.
    This does NOT persist anything.
    """

    campaigns = generate_campaign_recommendations()
    messages = generate_campaign_messages()
    message_map = {m["segment_id"]: m for m in messages}

    for c in campaigns:
        if c["segment_id"] != segment_id:
            continue

        roi = c["roi_estimation"]
        parameters = c["parameters"]
        message_payload = message_map.get(segment_id)

        if not message_payload:
            raise ValueError("Message generation failed for segment")

        return {
            "campaign_id": f"PREVIEW_{segment_id}",
            "segment_id": segment_id,
            "campaign_name": c["segment"],
            "channel": c["channel"],
            "audience_size": parameters["target_size"],
            "estimated_cost": roi["estimated_campaign_cost"],
            "estimated_response_rate": int(
                roi["estimated_participation_rate"] * 100
            ),
            "projected_roi": roi["estimated_roi"],
            "message": message_payload["message"],
            "cta": "Shop Now",
        }

    raise ValueError("No campaign found for given segment")


# -------------------------------------------------
# 2️⃣ CAMPAIGN LAUNCH (PHASE 5)
# -------------------------------------------------
def launch_campaign(segment_id: str, *, force_human: bool = False) -> dict:
    """
    Persist a campaign and mark it LIVE.

    Phase 5 responsibilities:
    - Decide autonomy vs human launch
    - Freeze AI preview
    - Execute campaign
    - Persist lifecycle + audit
    """

    preview = preview_campaign(segment_id)
    learning_signal = get_learning(segment_id)

    # ---- Autonomy decision ----
    is_autonomous = (
        not force_human
        and should_auto_launch(preview, learning_signal)
    )

    launch_mode = "AUTONOMOUS" if is_autonomous else "HUMAN_APPROVED"

    now = datetime.utcnow().isoformat()
    campaign_id = f"CMP_{uuid4().hex[:6].upper()}"

    campaign = {
        # ---- Identity ----
        "campaign_id": campaign_id,
        "segment_id": segment_id,
        "name": preview["campaign_name"],
        "channel": preview["channel"],

        # ---- AI predictions (immutable) ----
        "audience_size": preview["audience_size"],
        "estimated_cost": preview["estimated_cost"],
        "estimated_response_rate": preview["estimated_response_rate"],
        "projected_roi": preview["projected_roi"],

        # ---- Creative ----
        "message": preview["message"],
        "cta": preview["cta"],

        # ---- Lifecycle ----
        "status": "LIVE",
        "launch_mode": launch_mode,
        "created_at": now,
        "launched_at": now,

        # ---- Metrics ----
        "metrics": {
            "participants": 0,
            "revenue": 0,
            "actual_roi": None,
            "last_updated": None,
        },

        # ---- Explainability snapshot ----
        "explanation": {
            "why_launched": (
                "Autonomously launched by AI under policy guardrails"
                if launch_mode == "AUTONOMOUS"
                else "Approved by human after AI recommendation"
            ),
            "ai_projected_roi": preview["projected_roi"],
            "estimated_response_rate": preview["estimated_response_rate"],
        },
    }

    # ---- Persist campaign ----
    save_campaign(campaign)

    # ---- Execute campaign (stub / real later) ----
    execution_result = execute_campaign(campaign)
    campaign["execution"] = execution_result
    save_campaign(campaign)

    # ---- Audit log ----
    log_event(
        event_type="CAMPAIGN_LAUNCHED",
        payload={
            "campaign_id": campaign_id,
            "segment_id": segment_id,
            "launch_mode": launch_mode,
            "channel": campaign["channel"],
            "audience_size": campaign["audience_size"],
            "projected_roi": campaign["projected_roi"],
        },
    )

    return campaign


# -------------------------------------------------
# 3️⃣ CAMPAIGN DETAILS (LIVE METRICS)
# -------------------------------------------------
def get_campaign_details(campaign_id: str) -> dict:
    """
    Retrieve campaign details and refresh performance metrics.
    """

    campaign = get_campaign(campaign_id)
    if not campaign:
        raise ValueError("Campaign not found")

    campaign = refresh_campaign_metrics(campaign)
    return campaign


# -------------------------------------------------
# 4️⃣ LIST ALL CAMPAIGNS
# -------------------------------------------------
def list_campaigns() -> list[dict]:
    """
    Return all launched campaigns.
    """
    return get_all_campaigns()
