from typing import Optional

from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_name: Mapped[str] = mapped_column(String(50), comment="书名")
    author: Mapped[Optional[str]] = mapped_column(String(50), comment="作者")
    price: Mapped[Optional[float]] = mapped_column(Float, comment="价格")
    publish_house: Mapped[Optional[str]] = mapped_column(String(50), comment="出版社")
