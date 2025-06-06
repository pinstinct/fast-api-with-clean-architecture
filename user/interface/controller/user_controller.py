from datetime import datetime
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field

from common.auth import CurrentUser, get_admin_user, get_current_user
from containers import Container
from user.application.user_service import UserService

router = APIRouter(prefix="/users")


class CreateUserBody(BaseModel):
    """
    Pydantic: 데이터 유효성 검사와 직렬화/역직렬화를 위해 FastAPI가 기본으로 사용하는 라이브러리
    """
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    password: str = Field(min_length=8, max_length=32)


class UpdateUserBody(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    password: str | None = Field(min_length=8, max_length=32, default=None)


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: datetime


class GetUserResponse(BaseModel):
    total_count: int
    page: int
    users: list[UserResponse]


@router.post("", status_code=201)
@inject
def create_user(
    user: CreateUserBody,
    # background_tasks: BackgroundTasks,  # 엔드포인트 함수에서 Depends 없이 주입 받아야 한다.
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> UserResponse:
    created_user = user_service.create_user(name=user.name, email=user.email,
                                            password=user.password,
                                            # background_tasks=background_tasks,
                                            )
    return created_user


@router.put("")
@inject
def update_user(
        # get_current_user 수행 결과를 주입 받으므로, 따로 user_id를 전달받을 필요가 없다.
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        body: UpdateUserBody,
        user_service: UserService = Depends(Provide[Container.user_service]),
) -> UserResponse:
    user = user_service.update_user(
        user_id=current_user.id,
        name=body.name,
        password=body.password)
    return user


@router.get("")
@inject
def get_users(page: int = 1,
              items_per_page: int = 10,
              current_user: CurrentUser = Depends(get_admin_user),
              user_service: UserService = Depends(Provide[Container.user_service]),
              ) -> GetUserResponse:
    total_count, users = user_service.get_users(page, items_per_page)
    return {"total_count": total_count, "page": page, "users": users, }


# 204 No Content: 요청이 성공했으나 클라이언트가 현재 페이지에서 벗어나지 않아도 된다는 것을 나타냄
@router.delete("", status_code=204)
@inject
def delete_user(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        user_service: UserService = Depends(Provide[Container.user_service]), ):
    user_service.delete_user(current_user.id)


@router.post("/login")
@inject
def logi(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
         # form-data로 데이터를 전달받아야 하고, 데이터 형식은 username과 password로 고정, OAuth2 스펙에 정의
         user_service: UserService = Depends(Provide[Container.user_service]), ):
    access_token = user_service.login(
        email=form_data.username,
        password=form_data.password
    )

    return {"access_token": access_token, "token_type": "bearer"}  # OAuth2 스펙에 정의
