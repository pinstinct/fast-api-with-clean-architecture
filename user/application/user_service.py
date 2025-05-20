from datetime import datetime

from dependency_injector.wiring import inject
from fastapi import HTTPException
from ulid import ULID

from user.domain.repository.user_repo import InterfaceUserRepository
from user.domain.user import User
from utils.crypto import Crypto


class UserService:
    """
    ULID(Universally unique Lexicographically Sortable Identifier, 정렬 가능한 범용 고유 식별자):
    UUID(범용 고유 식별자)와 유사하지만, UUID보다 나은 점이 있다.
    UUID는 문자열이 너무 길어서 데이터가 많을 때 리소스가 낭비되고 성능에 문제가 생긴다.
    UUID4는 여러 대의 기기에서 동시에 생성할 경우 충돌의 위험이 있고, 완전히 임의의 문자열이기 때문에 데이터베이스 정렬 성능에 문제가 발생한다.
    ULID는 첫 48비트를 현재 타임스탬프 기반으로 생성한다. 때문에 검색 성능을 향상할 수 있다.
    """

    @inject  # 주입받은 객체를 사용한다고 선언
    # user_repo 팩토리를 선언해두었기 때문에 타입 선언만으로도 UserService가 생성될 때 팩토리를 수행한 객체가 주입
    def __init__(self, user_repo: InterfaceUserRepository):
        self.user_repo = user_repo  # 의존성 역전
        self.ulid = ULID()
        self.crypto = Crypto()

    def create_user(
        self,name: str,email: str,password: str,memo: str | None = None,
    ):
        _user = None  # 데이터베이스에서 찾은 유저

        try:
            _user = self.user_repo.find_by_email(email)
        except HTTPException as e:
            if e.status_code != 422:
                raise e

        if _user:
            # 422(Unprocessable Content): 서버가 요청 엔티티 콘텐츠 형식을 이해했고 요청 엔티티의 문법도 올바르지만
            # 요청된 지시를 처리할 수 없음
            raise HTTPException(status_code=422)

        now = datetime.now()
        user: User = User(
            id=self.ulid.generate(),
            name=name,
            email=email,
            password=self.crypto.encrypt(password),
            memo=memo,
            created_at=now,
            updated_at=now,
        )
        self.user_repo.save(user)
        return user

    def update_user(
        self,
        user_id: str,
        name: str | None = None,
        password: str | None = None,
        memo: str | None = None,
    ):
        user = self.user_repo.find_by_id(user_id)

        if name:
            user.name = name
        if password:
            user.password = self.crypto.encrypt(password)
        user.updated_at = datetime.now()

        self.user_repo.update(user)

        return user
