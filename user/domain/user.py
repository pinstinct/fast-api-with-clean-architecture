from dataclasses import dataclass
from datetime import datetime


@dataclass  # 도메인 객체를 다루기 위한 데코레이터
class User:
    id: str
    name: str
    email: str
    password: str
    memo: str | None
    created_at: datetime
    updated_at: datetime
