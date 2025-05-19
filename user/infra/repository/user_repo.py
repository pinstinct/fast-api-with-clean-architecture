from fastapi import HTTPException

from database import SessionLocal
from user.domain.repository.user_repo import InterfaceUserRepository
from user.domain.user import User as UserVO  # 데이터베이스 모델과 구분하기 위해 VO 접미어를 붙임
from user.infra.db_models.user import User
from utils.db_utils import row_to_dict


class UserRepository(InterfaceUserRepository):

    def save(self, user: UserVO):
        new_user = User(
            id=user.id,
            email=user.email,
            name=user.name,
            password=user.password,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

        with SessionLocal() as db:  # with 구문을 사용해 세션 자동 종료
            db = SessionLocal()  # SessionLocal을 이용해 새로운 세션 생성
            db.add(new_user)
            db.commit()

    def find_by_email(self, email: str) -> UserVO:
        with SessionLocal() as db:
            user = db.query(User).filter(User.email == email).first()  # 없는 경우 None 반환

        if not user:
            raise HTTPException(status_code=422)

        return UserVO(**row_to_dict(user))
