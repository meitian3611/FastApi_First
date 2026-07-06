from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ApiError
from app.models import Book
from app.schemas.book_schemas import BookCreate, DeleteBook, BookEdit


# 封装 统一获取书本  id
async def get_book_by_id(db: AsyncSession, book_id: int) -> Book:
    book = await db.get(Book, book_id)
    if book is None:
        raise ApiError(msg="书本不存在", code=400)

    return book


# 封装 统一获取书本 name
async def get_book_by_name(db: AsyncSession, book_name: str) -> Book | None:
    stmt = select(Book).where(Book.book_name == book_name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# 获取书本：不传 book_id 就查全部
async def get_book_list(db: AsyncSession, filter_params) -> list[Book]:
    book_id = filter_params.id

    if book_id is not None:
        result = await db.execute(select(Book).where(Book.id == book_id))
        return list(result.scalars().all())

    result = await db.execute(select(Book))
    return list(result.scalars().all())


# 添加书本
async def create_book(db: AsyncSession, payload: BookCreate) -> Book:
    # 判断书本是否存在
    if await get_book_by_name(db, payload.book_name):
        raise ApiError(msg="书本已存在 请重新添加", code=400)

    book = Book(**payload.model_dump())  # 模型字段与 payload 字段一致

    db.add(book)

    await db.flush()
    await db.refresh(book)

    return book


# 删除
async def delete_book(db: AsyncSession, payload: DeleteBook) -> None:
    book = await get_book_by_id(db, payload.id)

    await db.delete(book)


# 修改
async def update_book(db: AsyncSession, payload: BookEdit) -> None:
    book = await get_book_by_id(db, payload.id)

    update_data = payload.model_dump(exclude_unset=True, exclude={"id"}, exclude_none=True)  # 忽略未设置字段
    for key, value in update_data.items():  # 遍历更新字段
        setattr(book, key, value)

    await db.flush()
    await db.refresh(book)
