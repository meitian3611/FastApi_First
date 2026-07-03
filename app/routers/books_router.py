from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models import Book
from app.schemas import BookCreate, BookOut

# 每个资源一个 router；prefix 统一起始路径，tags 用于文档分组
router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=List[BookOut])
async def list_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book))
    return result.scalars().all()


@router.post("", response_model=BookOut)
async def create_book(payload: BookCreate, db: AsyncSession = Depends(get_db)):
    book = Book(**payload.model_dump())
    db.add(book)
    await db.commit()
    await db.refresh(book)  # server_default 时间字段需 refresh 取值
    return book
