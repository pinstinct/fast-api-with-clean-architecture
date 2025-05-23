from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from starlette import status

from config import get_settings

settings = get_settings()

SECRET_KEY = settings.jwt_secret
ALGORITHM = "HS256"


class Role(StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"


def create_access_token(
        payload: dict,
        role: Role,
        expires_delta: timedelta = timedelta(
            hours=6),
):
    expire = datetime.utcnow() + expires_delta
    payload.update({"role": role, "exp": expire, })  # 6시간 후 만료
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


# OAuth2PasswordBearer 클래스를 이용해 아이디, 패스워드 기반으로 로그인 가능
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


@dataclass
class CurrentUser:
    id: str
    role: Role

    def __str__(self):
        return f"{self.id}({self.role})"


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """oauth2_scheme을 통해 얻은 토큰을 복호화한 페이로드에서 현재 유저 정보를 구한다."""
    payload = decode_access_token(token)
    user_id = payload.get("user_id")
    role = payload.get("role")
    if not user_id or not role or role != Role.USER:
        # 403 Forbidden: 서버에 요청이 전달되었지만, 권한 때문에 거절되었다는 것을 의미
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return CurrentUser(user_id, Role(role))


def get_admin_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_access_token(token)
    role = payload.get("role")
    if not role or role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return CurrentUser("ADMIN_USER_ID", role)
