# services/idempotency_service.py

IDEMPOTENCY_KEYS = set()


def check_and_register(key: str) -> bool:
    if key in IDEMPOTENCY_KEYS:
        return False
    IDEMPOTENCY_KEYS.add(key)
    return True
