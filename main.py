import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from containers import Container
from example.async_ex import router as async_ex_routers
from example.sync_ex import router as sync_ex_routers
from user.interface.controller.user_controller import router as user_routers

app = FastAPI()
app.include_router(user_routers)
app.include_router(sync_ex_routers)
app.include_router(async_ex_routers)
app.container = Container()  # 어플리케이션 구동 시, 작성한 컨테이너 클래스 등록


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content=exc.errors())


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
