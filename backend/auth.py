import hmac
import os
from fastapi import Header, HTTPException


def verify_token(authorization: str = Header(None)) -> None:
    secret = os.getenv("PALANTIR_SECRET", "")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(" ", 1)[1]
    if not hmac.compare_digest(token.encode(), secret.encode()):
        raise HTTPException(status_code=401, detail="Unauthorized")
