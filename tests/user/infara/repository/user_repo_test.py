from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException

from user.domain.user import User as UserVO
from user.infra.db_models.user import User
from user.infra.repository.user_repo import UserRepository
from utils.db_utils import row_to_dict


@pytest.fixture
def mock_session_local():  # SQLAlchmey 세션을 모의한 픽스처 제공
    with patch(
            "user.infra.repository.user_repo.SessionLocal", autospec=True
    ) as mock_session:
        yield mock_session


def test_find_by_email_user_exists(mock_session_local):
    mock_user = User(
        id=1, email="test@example.com", name="Test User"
    )
    mock_db = Mock()  # pytest-mock 패키지의 mocker 대신 unittest의 Mock 클래스 이용해 모의 객체 생성

    # 유저 저장소가 검색 결과로 반환하는 유저 도메인 객체를 모의
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    # 생성되는 세션을 모의
    mock_session_local.return_value.__enter__.return_value = mock_db
    user_repository = UserRepository()

    # 테스트 대상 코드를 호출
    result = user_repository.find_by_email("test@example.com")

    # 결과 비교
    assert result == UserVO(**row_to_dict(mock_user))


def test_find_by_email_user_does_not_exist(mock_session_local):
    mock_db = Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_session_local.return_value.__enter__.return_value = mock_db
    user_repository = UserRepository()

    # 예외가 일어나는지 확인
    with pytest.raises(HTTPException) as e:
        user_repository.find_by_id("test@test.com")

    # 일어난 예외의 상태 코드가 원하는 값인지 확인
    assert e.value.status_code == 422
