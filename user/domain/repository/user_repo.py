from abc import ABCMeta, abstractmethod

from user.domain.user import User


class InterfaceUserRepository(metaclass=ABCMeta):
    """
    User 도메인을 영속화하기 위한 모듈
    추상 클래스이므로 객체를 직접 생성할 수 없다. 또한 구현체는 이 함수를 구현하지 않으면 에러가 발생한다.
    """

    @abstractmethod  # 구현체에서 구현할 함수
    def save(self, user: User):
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email: str) -> User:
        """
        이메일로 유저를 검색한다.
        검색한 유저가 없을 경우 422 에러를 발생시킨다.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User):
        raise NotImplementedError

    @abstractmethod
    def get_users(self, page: int, items_per_page: int) -> tuple[int, list[User]]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str):
        raise NotImplementedError
