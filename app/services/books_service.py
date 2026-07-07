from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ApiError
from app.models import Book
from app.schemas.book_schemas import BookCreate, DeleteBook, BookEdit, FilterParams
from app.services.utils.paginate import pageInit, apply_sort


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


# 可以进行排序的字段
SORT_FIELDS = {
    "id": Book.id,
    "book_name": Book.book_name,
    "price": Book.price,
    "create_time": Book.create_time,
    "update_time": Book.update_time,
}


# 获取书本：不传 book_id 就查全部
async def get_book_list(db: AsyncSession, filter_params: FilterParams) -> list[Book]:
    stmt = select(Book)

    if filter_params.id is not None:
        stmt = stmt.where(Book.id == filter_params.id)

    if filter_params.book_name:
        stmt = stmt.where(Book.book_name.like(f"%{filter_params.book_name}%"))  # like 模糊查询

    if filter_params.order_by:
        stmt = await apply_sort(stmt, filter_params, SORT_FIELDS)

    return await pageInit(db=db, stmt=stmt, page=filter_params.page, page_size=filter_params.page_size)  # 分页


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
