# agents/message_agent.py

from agents.strategy_agent import recommend_campaign_strategies
from agents.llm_client import get_groq_client, get_groq_model


MAX_WORDS = 45  # slightly longer, still SMS/email safe


def generate_campaign_messages() -> list[dict]:
    """
    Generate human-friendly, slightly more detailed campaign messages
    using an LLM. Messages remain channel-appropriate and controlled.
    """

    client = get_groq_client()
    model = get_groq_model()

    strategies = recommend_campaign_strategies()
    results: list[dict] = []

    for strategy in strategies:
        try:
            prompt = f"""
You are an expert marketing copywriter for a customer loyalty program.

Context:
- Customer segment: {strategy['segment_name']}
- Campaign type: {strategy['campaign_type']}
- Communication channel: {strategy['channel']}
- Audience: loyalty members
- Objective: re-engagement or value reinforcement

Guidelines:
- Do NOT mention internal segment names or analytics
- Do NOT change campaign type or channel
- Keep the message under {MAX_WORDS} words
- Be clear, warm, and action-oriented
- Include a subtle incentive or value reminder if appropriate
- Avoid slang and emojis

Write ONE ready-to-send customer message.
"""

            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=120,
            )

            raw_message = response.choices[0].message.content.strip()
            message = raw_message.strip('"').strip("'")

        except Exception as e:
            message = (
                "We have a special update for you. "
                "Visit us today to enjoy exclusive benefits and rewards."
            )

        results.append({
            "segment_id": strategy["segment_id"],
            "segment_name": strategy["segment_name"],
            "campaign_type": strategy["campaign_type"],
            "channel": strategy["channel"],
            "message": message,
            "reason": strategy["reason"],
        })

    return results
