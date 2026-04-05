from jose import jwt, JWTError
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import get_session
from sqlmodel import Session
from app.models.user import User
import uuid

SUPABASE_JWT_PUBLIC_KEY: dict[str, str | bool | list[str]] = {
    "x": "IY81RMTdBpZwWkto4inAxPzy4-MhgpP8iaapHK2RS2Q",
    "y": "ia-qUg6oHN57f_RFsL9tjhExiSxvJxVNJw6Gk2GjxN0",
    "alg": "ES256",
    "crv": "P-256",
    "ext": True,
    "kid": "39c9edba-b4e3-40a2-b3e4-cb62dbe3c556",
    "kty": "EC",
    "key_ops": ["verify"],
}

ALGORITHM = "ES256"
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session),
) -> User:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_PUBLIC_KEY,
            algorithms=[ALGORITHM],
            audience="authenticated",
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
        )

    user = session.get(User, uuid.UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user
