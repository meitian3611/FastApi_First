from typing import List, Union

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.response import ApiResponse, success, fail
from app.schemas import BookCreate, BookOut, DeleteBook, BookEdit
from app.services import create_book, get_book_list, delete_book, update_book

"""
    router 只做参数校验与调用 service，业务逻辑下沉到 app/services
"""

# 每个资源一个 router；prefix 统一起始路径，tags 用于文档分组
router = APIRouter(prefix="/books", tags=["books"])


# 获取书本：不传 book_id 就查全部
@router.get("/query", response_model=ApiResponse[List[BookOut]])
async def list_books(db: AsyncSession = Depends(get_db), book_id: int | None = None, ):
    return success(await get_book_list(db, book_id))


# 添加书本
@router.post("/add", response_model=ApiResponse[BookOut])
async def add_book(payload: BookCreate, db: AsyncSession = Depends(get_db)):
    return success(await create_book(db, payload))


# 删除书本
@router.post("/delete")
async def del_book(payload: DeleteBook, db: AsyncSession = Depends(get_db)):
    book = await get_book_list(db, payload.id)
    if not book:
        return fail(msg="书本不存在")
    return success(await delete_book(db, payload))


# 修改书本信息
@router.post("/update")
async def edit_book(payload: BookEdit, db: AsyncSession = Depends(get_db)):
    book = await get_book_list(db, payload.id)
    if not book:
        return fail(msg="书本不存在")
    return success(await update_book(db, payload))
