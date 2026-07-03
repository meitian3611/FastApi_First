from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.response import ApiResponse, success
from app.schemas import BookCreate, BookOut
from app.services import create_books, get_books

# 每个资源一个 router；prefix 统一起始路径，tags 用于文档分组
# router 只做参数校验与调用 service，业务逻辑下沉到 app/services
router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=ApiResponse[List[BookOut]])
async def list_books(db: AsyncSession = Depends(get_db)):
    return success(await get_books(db))


@router.post("", response_model=ApiResponse[BookOut])
async def create_book(payload: BookCreate, db: AsyncSession = Depends(get_db)):
    return success(await create_books(db, payload))
