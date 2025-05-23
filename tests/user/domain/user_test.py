from datetime import datetime

from user.domain.user import User


def test_user_creation():
    """
    이 테스트 코드는 비즈니스 로직을 테스트하는 게 아니라 파이썬 내장 모듈을 테스트하고 있다.
    즉, 어떤 클래스가 dataclass로 선언돼 있을 때 객체가 잘 생성되는지를 테스트한다.
    """
    user = User(
        id="ID_DEXTER",
        name="DEXTER",
        email="dexter@example.com",
        password="testtest",
        memo=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    assert user.id == "ID_DEXTER"
    assert user.name == "DEXTER"
    assert user.email == "dexter@example.com"
    assert user.password == "testtest"
    assert user.memo is None
