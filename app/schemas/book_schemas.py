from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


# 请求体：创建书本时前端提交的字段
class BookCreate(BaseModel):
    book_name: str
    author: Optional[str] = None
    price: Optional[float] = None
    publish_house: Optional[str] = None


# 响应模型：from_attributes=True 允许直接读 ORM 对象来序列化
class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True) # 允许直接读 ORM 模型对象来序列化
    id: int
    book_name: str
    author: Optional[str] = None
    price: Optional[float] = None
    publish_house: Optional[str] = None
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None


class DeleteBook(BaseModel):
    id: int


# 修改请求体
class BookEdit(BaseModel):
    id: int
    book_name: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None
    publish_house: Optional[str] = None
