from celery import Celery

from config import get_settings
from user.application.send_welcome_email_task import SendWelcomeEmailTask

settings = get_settings()

# 셀러리 객체 생성
celery = Celery(
    "fastapi-ca",  # 앱 이름
    broker=settings.celery_broker_url,
    backend=settings.celery_backend_url,

    # 워커가 수행될 때 브로커와의 연결이 제대로 이루어지지 않으면 재시도를 수행할지에 대한 설정
    broker_connection_retry_on_startup=True,

    # 샐러리 태스크가 정의된 모듈을 지정
    include=["example.celery_task"],
)

celery.register_task(SendWelcomeEmailTask())
