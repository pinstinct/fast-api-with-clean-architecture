from dependency_injector import containers, providers

from note.application.note_service import NoteService
from note.infra.repository.note_repo import NoteRepository
from user.application.user_service import UserService
from user.infra.repository.user_repo import UserRepository


class Container(containers.DeclarativeContainer):
    """
    dependency-injector는 IoC 컨테이너를 제공한다.
    애플리케이션이 구동될 때 IoC 컨테이너에 미리 의존성을 제공하는 객체를 등록해두고 필요한 모듈에서 주입하도록 할 수 있다.
    이렇게 되면 주입할 때의 타입을 인터페이스로 선언하더라도 실제로 주입되는 객체는 구현체가 되도록 할 수 있게 한다.
    """
    # 의존성을 사용할 모듈 선언
    wiring_config = containers.WiringConfiguration(packages=["user", "note", ], )

    # 의존성을 제공할 모듈을 팩토리에 등록
    # providers 모듈에는 다양한 종류의 프로바이더를 제공
    # Factory: 객체를 매번 생성
    # Singleton: 처음 호출될 때 생성한 객체를 재활용
    user_repo = providers.Factory(UserRepository)
    user_service = providers.Factory(UserService, user_repo=user_repo)
    note_repo = providers.Factory(NoteRepository)
    note_service = providers.Factory(NoteService, note_repo=note_repo)
