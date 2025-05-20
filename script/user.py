import os.path
import sys
from datetime import datetime

from database import SessionLocal
from user.infra.db_models.user import User
from utils.crypto import Crypto

# 실행 시, 위치를 패키지 import 위로 올린다
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, ROOT_DIR)  # import문의 모듈을 찾을 때 참조하는 경로 리스트에 ROOT_DIR 추가


if __name__ == "__main__":
    with SessionLocal() as db:
        for i in range(50):
            user = User(
                id=f"UserID-{str(i).zfill(2)}",
                name=f"TestUser{i}",
                email=f"test-user{i}@test.com",
                password=Crypto().encrypt("test"),
                memo=None,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            db.add(user)
        db.commit()
