from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ApiError
from app.models import Book
from app.schemas import BookCreate, DeleteBook, BookEdit


# 获取书本：不传 book_id 就查全部
async def get_book_list(db: AsyncSession, book_id: int | None = None) -> list[Book]:
    if book_id is not None:
        result = await db.execute(select(Book).where(Book.id == book_id))
        return list(result.scalars().all())

    result = await db.execute(select(Book))
    return list(result.scalars().all())


# 添加书本
async def create_book(db: AsyncSession, payload: BookCreate) -> Book:
    book = Book(**payload.model_dump()) # 模型字段与 payload 字段一致
    db.add(book)

    await db.flush()
    await db.refresh(book)
    return book


# 删除
async def delete_book(db: AsyncSession, payload: DeleteBook) -> Book:
    book = await db.get(Book, payload.id)
    return await db.delete(book)


# 修改
async def update_book(db: AsyncSession, payload: BookEdit) -> Book:
    book = await db.get(Book, payload.id)

    update_data = payload.model_dump(exclude_unset=True) # 忽略未设置字段
    update_data.pop("id", None) # 忽略 id
    for key, value in update_data.items(): # 遍历更新字段
        setattr(book, key, value)

    await db.flush()
    await db.refresh(book)
    return
