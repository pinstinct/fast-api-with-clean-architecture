import time

from fastapi import FastAPI
from starlette.requests import Request


def create_sample_middleware(app: FastAPI):  # main.py에서 생성한 FastAPI 객체를 전달 받는다.

    @app.middleware("http")  # 미들웨어임을 알림
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()

        # 미들웨어가 여러 개 등록돼 있다면 다음 미들웨어로 요청 객체 전달
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        return response
