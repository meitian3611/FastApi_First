from typing import Optional
from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


# User 类对应数据库里的 user 表；__tablename__ 是真实表名
class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), comment="用户名")
    password: Mapped[str] = mapped_column(String(50), comment="密码")
    age: Mapped[Optional[int]] = mapped_column(nullable=True, comment="年龄")
    sex: Mapped[Optional[str]] = mapped_column(String(20), comment="性别")
