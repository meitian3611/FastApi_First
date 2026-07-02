from datetime import datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 异步驱动 mysql+aiomysql；密码写死仅供学习，正式项目放 .env
DATABASE_URL = "mysql+aiomysql://root:123456@127.0.0.1:3306/FastApi"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # 打印SQL（上线建议关掉）
    pool_size=10,
    max_overflow=20,
)

# 每次请求用 SessionLocal() 拿到一个 AsyncSession
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


# AsyncAttrs + DeclarativeBase 是异步环境下推荐的基类写法
class Base(AsyncAttrs, DeclarativeBase):
    # 数据库侧默认值：时间由 DB 计算，任何写库方式都生效（含批量 UPDATE）
    # 注意：插入/更新后对象上不会自动有值，需 db.refresh(obj) 读回
    create_time: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP"), comment="创建时间"
    )
    update_time: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        comment="更新时间",
    )


# 启动时为 Base 下所有模型建表（异步写法）
async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# 依赖项：每个请求创建一个 AsyncSession，请求结束自动关闭
async def get_db():
    async with SessionLocal() as session:
        yield session
