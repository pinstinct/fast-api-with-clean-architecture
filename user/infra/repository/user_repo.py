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
            memo=user.memo,
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

    def find_by_id(self, id: str) -> User:
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == id).first()

        if not user:
            raise HTTPException(status_code=422)

        return UserVO(**row_to_dict(user))

    def update(self, user_vo: UserVO):
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_vo.id).first()

            if not user:
                raise HTTPException(status_code=422)

            user.name = user_vo.name
            user.password = user_vo.password
            db.add(user)
            db.commit()
        return user

    def get_users(self,
                  page: int = 1,
                  items_per_page: int = 10) -> tuple[int, list[UserVO]]:
        with SessionLocal() as db:
            query = db.query(User)
            total_count = query.count()

            offset = (page - 1) * items_per_page
            users = query.limit(items_per_page).offset(offset).all()
        return total_count, [UserVO(**row_to_dict(user)) for user in users]

    def delete(self, id: str):
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == id).first()

            if not user:
                raise HTTPException(status_code=422)

            db.delete(user)
            db.commit()
