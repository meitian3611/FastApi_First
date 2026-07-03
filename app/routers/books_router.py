from typing import List, Union

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.response import ApiResponse, success, fail
from app.schemas import BookCreate, BookOut
from app.services import create_books, get_book_list

# 每个资源一个 router；prefix 统一起始路径，tags 用于文档分组
router = APIRouter(prefix="/books", tags=["books"])

"""
    router 只做参数校验与调用 service，业务逻辑下沉到 app/services
"""


# 获取书本：不传 book_id 就查全部
@router.get("/query", response_model=ApiResponse[List[BookOut]])
async def list_books(db: AsyncSession = Depends(get_db), book_id: int | None = None, ):
    return success(await get_book_list(db, book_id))


@router.post("/add", response_model=ApiResponse[BookOut])
async def create_book(payload: BookCreate, db: AsyncSession = Depends(get_db)):
    return success(await create_books(db, payload))
