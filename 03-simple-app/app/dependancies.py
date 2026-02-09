from datetime import datetime, timezone
def utcnow() -> datetime:
    return datetime.now(timezone.utc)

def limit_params(offset: int, skip: int):
    return {"offset": offset, "limit": offset + skip}