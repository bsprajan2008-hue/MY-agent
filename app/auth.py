import hmac
import hashlib
import base64
import json
import time
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, Depends, status
from app.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from app.database import get_db

def hash_password(password: str) -> str:
    salt = hashlib.sha256(SECRET_KEY.encode()).hexdigest()[:16]
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"{salt}${key.hex()}"

def verify_password(password: str, hashed: str) -> bool:
    try:
        if not hashed or '$' not in hashed:
            return False
        salt, key_hex = hashed.split('$', 1)
        expected_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return hmac.compare_digest(expected_key.hex(), key_hex)
    except Exception:
        return False

def create_session_token(user_id: str, org_id: str, role: str) -> str:
    expires_at = int(time.time()) + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    payload = {
        "uid": user_id,
        "oid": org_id,
        "rol": role,
        "exp": expires_at
    }
    encoded_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
    sig = hmac.new(SECRET_KEY.encode(), encoded_payload.encode(), hashlib.sha256).hexdigest()
    return f"{encoded_payload}.{sig}"

def decode_session_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        if not token or '.' not in token:
            return None
        encoded_payload, sig = token.split('.', 1)
        expected_sig = hmac.new(SECRET_KEY.encode(), encoded_payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected_sig):
            return None
        
        # Add padding back if necessary
        rem = len(encoded_payload) % 4
        padded = encoded_payload + ('=' * (4 - rem) if rem else '')
        payload = json.loads(base64.urlsafe_b64decode(padded).decode())
        
        if payload.get("exp", 0) < time.time():
            return None
        return payload
    except Exception:
        return None

def get_current_user_from_token(token: Optional[str]) -> Optional[Dict[str, Any]]:
    if not token:
        return None
    payload = decode_session_token(token)
    if not payload:
        return None
    user_id = payload.get("uid")
    if not user_id:
        return None
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.*, d.name as department_name, o.name as org_name, o.industry as org_industry
            FROM users u
            JOIN organisations o ON u.org_id = o.id
            LEFT JOIN departments d ON u.department_id = d.id
            WHERE u.id = ?
        """, (user_id,))
        user = cursor.fetchone()
        return user

def get_current_user(request: Request) -> Dict[str, Any]:
    token = request.cookies.get("fairshift_session")
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
            
    user = get_current_user_from_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def require_role(*allowed_roles: str):
    def role_checker(user: Dict[str, Any] = Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Requires one of roles: {', '.join(allowed_roles)}. Current role: {user['role']}"
            )
        return user
    return role_checker
