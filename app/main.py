import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.db import create_table
from app.core.response import success
from app.core.exception_handlers import register_exception_handlers
from app.routers import all_routers
import app.models  # 必须导入，否则 user/book 表不会注册到 Base


# 应用生命周期：启动建表，之后进入运行期
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    print("服务启动成功")
    yield


app = FastAPI(lifespan=lifespan)

# 全局异常处理器统一在 core/exception_handlers.py 定义并注册
register_exception_handlers(app)

# 挂载所有路由；新增资源只需在 app/routers/__init__.py 登记
for router in all_routers:
    app.include_router(router)


@app.get("/")
async def root():
    return success({"message": "Hello FastApi"})


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
