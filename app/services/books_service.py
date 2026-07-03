from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Book
from app.schemas import BookCreate


async def get_books(db: AsyncSession) -> list[Book]:
    result = await db.execute(select(Book))
    return list(result.scalars().all())


async def create_books(db: AsyncSession, payload: BookCreate) -> Book:
    book = Book(**payload.model_dump())
    db.add(book)
    await db.commit()
    await db.refresh(book)  # server_default 时间字段需 refresh 取值
    return book
