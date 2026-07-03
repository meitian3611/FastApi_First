from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.db import create_table
from app.routers import all_routers
import app.models  # 必须导入，否则 user/book 表不会注册到 Base


# 应用生命周期：yield 前启动建表，之后进入运行期
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    print("服务启动成功")
    yield


fastapi = FastAPI(lifespan=lifespan)

# 挂载所有路由；新增资源只需在 app/routers/__init__.py 登记
for router in all_routers:
    fastapi.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello FastApi"}
