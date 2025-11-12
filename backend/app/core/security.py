from datetime import datetime, timedelta, timezone
import jwt
from .config import get_settings

def create_jwt(sub: str, minutes: int = 60) -> str:
    s = get_settings()
    now = datetime.now(tz=timezone.utc)
    payload = {"sub": sub, "iat": int(now.timestamp()), "exp": int((now + timedelta(minutes=minutes)).timestamp())}
    return jwt.encode(payload, s.jwt_secret, algorithm=s.jwt_alg)

def verify_jwt(token: str) -> dict:
    s = get_settings()
    return jwt.decode(token, s.jwt_secret, algorithms=[s.jwt_alg])
