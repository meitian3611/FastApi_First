from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from .common_schemas import BaseSchema

"""
    请求模型
    前端需要传给接口的
"""


# 新增 - 书本时前端提交的字段
class BookCreate(BaseModel):
    book_name: str
    author: Optional[str] = None
    price: Optional[float] = None
    publish_house: Optional[str] = None


# 查询 - 前端传递的参数模型
class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}  # 不允许传入未定义的接口参数
    id: int | None = None
    book_name: str | None = None
    page: int = 1
    page_size: int = 10

    order_by: str | None = None
    order: str | None = None


# 修改
class BookEdit(BaseModel):
    id: int
    book_name: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None
    publish_house: Optional[str] = None


# 删除
class DeleteBook(BaseModel):
    id: int


"""
    响应模型
    接口返回给前端的
"""


# 响应模型：from_attributes=True 允许直接读 ORM 对象来序列化
# @field_serializer 函数处理字段 用来格式化指定字段
class BookOut(BaseSchema):
    id: int
    book_name: str
    author: Optional[str] = None
    price: Optional[float] = None
    publish_house: Optional[str] = None
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

