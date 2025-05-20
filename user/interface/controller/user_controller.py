from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from containers import Container
from user.application.user_service import UserService

router = APIRouter(prefix="/users")


class CreateUserBody(BaseModel):
    """
    Pydantic: 데이터 유효성 검사와 직렬화/역직렬화를 위해 FastAPI가 기본으로 사용하는 라이브러리
    """
    name: str
    email: str
    password: str


class UpdateUser(BaseModel):
    name: str | None = None
    password: str | None = None


@router.post("", status_code=201)
@inject
def create_user(user: CreateUserBody,
                user_service: UserService = Depends(Provide[Container.user_service])):
    created_user = user_service.create_user(name=user.name, email=user.email,
                                            password=user.password)
    return created_user


@router.put("/{user_id}")
@inject
def update_user(user_id: str, user: UpdateUser,
                user_service: UserService = Depends(Provide[Container.user_service])):
    user = user_service.update_user(
        user_id=user_id,
        name=user.name,
        password=user.password)
    return user
