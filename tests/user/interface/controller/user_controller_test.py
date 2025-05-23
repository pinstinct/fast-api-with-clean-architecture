import pytest

from user.application.user_service import UserService
from user.domain.user import User
from user.interface.controller import user_controller


@pytest.fixture
def user_interface_dependencies(mocker):
    user_service_mock = mocker.Mock(spec=UserService)
    user_mock = User(
        id="TEST_ID",
        name="Dexter",
        email="dexter.hann@test.com",
        password="password",
        memo="memo",
        created_at="created_at",
        updated_at="updated_at",
    )

    return user_service_mock, user_mock


def test_create_user(user_interface_dependencies):
    (user_service_mock, user_mock) = user_interface_dependencies
    user_service_mock.create_user.return_value = user_mock

    # 테스트 대상 함수 호출
    user_controller.create_user(
        user=user_controller.CreateUserBody(
            name="Dexter",
            email="dexter.hann@test.com",
            password="password",
        ),
        user_service=user_service_mock,
    )

    # create_user 함수가 호출되는지 확인
    user_service_mock.create_user.assert_called_once()
