import asyncio
from contextvars import ContextVar

from fastapi import APIRouter

# ContextVar 생성자의 첫 번째 인수는 콘텍스트 변수 이름
foo_context: ContextVar[str] = ContextVar("foo", default="bar")

router = APIRouter(prefix="/context")


@router.get("")
async def context_test(var: str):
    foo_context.set(var)  # 콘텍스트 변수의 값으로 설정
    await asyncio.sleep(1)

    return {
        "var": var,
        # 여러 요청이 동시에 수행되었을 때 잘 유지되는지 확인
        "context_var": foo_context.get(),
    }
