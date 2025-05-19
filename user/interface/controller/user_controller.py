from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from user.application.user_service import UserService

router = APIRouter(prefix="/users")


class CreateUserBody(BaseModel):
    """
    Pydantic: 데이터 유효성 검사와 직렬화/역직렬화를 위해 FastAPI가 기본으로 사용하는 라이브러리
    """
    name: str
    email: str
    password: str


@router.post("", status_code=201)
def create_user(user: CreateUserBody, user_service: Annotated[UserService, Depends(UserService)]):
    created_user = user_service.create_user(name=user.name, email=user.email,
                                            password=user.password)
    return created_user
