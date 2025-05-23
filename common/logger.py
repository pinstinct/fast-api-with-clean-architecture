import logging

from context_vars import user_context

# %(asctime)s: 사람이 읽을 수 있는 생성 시간
# %(name)s: 로깅 호출에 사용된 로거의 이름
# %(levelname)s: 로깅 수준
# %(message)s: 로그 메시지
log_format = "%(asctime)s %(name)s %(levelname)s:\tuser: %(user)s: %(message)s"


class CustomFormatter(logging.Formatter):
    """커스텀 포매터
    기본 포매터를 상속받아 정의한다. log_format에 %(user)s가 있는데,
    이 때문에 파일을 저장할 때 유비콘이 새로 시작되는 과정에서 에러가 발생하기 때문이다.
    따라서 LogRecord가 우리가 추가한 user 속성이 없는 경우를 처리해준다.
    """

    def format(self, record):
        if not hasattr(record, "user"):
            record.user = "Anonymous"
        return super().format(record)


# 커스텀 핸들러
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter(log_format))

# 커스텀 로거 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)  # 핸들러 추가


class ContextFilter(logging.Filter):
    """커스텀 콘텍스트 필터
    filter 함수에 전달되는 LogRecord 객체에 우리가 원하는 user 속성을 추가한다.
    LogRecord 객체의 user 속성은 log_format에서 사용되는 문자열이다. 따라서 콘텍스트 변수에서 가져온 CurrentUser 객체를 문자열로 변환해주어야 한다.
    이를 위해 CurrentUSer 클래스에 __str__ 함수를 추가하자.
    """

    def filter(self, record: logging.LogRecord):
        record.user = str(user_context.get())
        return True


# 커스텀 콘텍스트 필터를 로거에 추가
logger.addFilter(ContextFilter())
