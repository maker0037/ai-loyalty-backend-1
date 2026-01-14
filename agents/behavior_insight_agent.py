# agents/behavior_insight_agent.py

from agents.behavior_change_agent import detect_behavior_changes
from agents.segmentation_agent import segment_customers
from agents.llm_client import get_groq_client, get_groq_model


def generate_behavior_insights() -> dict:
    """
    Generate human-readable explanations for customer behavior changes
    at the segment level using an LLM.
    """

    client = get_groq_client()
    model = get_groq_model()

    behavior_signals = detect_behavior_changes()
    segments = segment_customers()

    # Map customer_id -> signals
    customer_signals: dict[str, list[str]] = {}
    customer_features: dict[str, dict] = {}

    for signal in behavior_signals:
        cid = signal["customer_id"]
        customer_signals.setdefault(cid, []).append(signal["signal"])
        customer_features[cid] = signal["features"]

    insights: dict[str, str] = {}

    for segment_id, segment_data in segments.items():
        customers = segment_data.get("customers", [])
        if not customers:
            continue

        # Aggregate signals & features at segment level
        segment_signals = set()
        feature_samples = []

        for cid in customers:
            segment_signals.update(customer_signals.get(cid, []))
            if cid in customer_features:
                feature_samples.append(customer_features[cid])

        if not segment_signals or not feature_samples:
            continue

        # Use first feature set as representative (demo-safe)
        f = feature_samples[0]

        try:
            prompt = f"""
You are a customer analytics expert.

Context:
- Segment: {segment_data['name']}
- Observed behavior signals: {', '.join(segment_signals)}

Key metrics:
- Days since last purchase: {f.get('days_since_last_purchase')}
- Purchases in last 30 days: {f.get('purchase_count_30d')}
- Average order value: {f.get('avg_order_value')}
- Dominant category: {f.get('dominant_category')}

Task:
Explain in 1–2 concise sentences why this segment's behavior
has changed or requires attention.

Rules:
- Do NOT mention internal system terms
- Do NOT mention customer IDs
- Be neutral, analytical, and business-friendly
"""

            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=120,
            )

            insight = response.choices[0].message.content.strip()

        except Exception:
            insight = (
                "This segment shows behavioral changes based on recent activity "
                "patterns and purchasing frequency."
            )

        insights[segment_id] = insight

    return insights
