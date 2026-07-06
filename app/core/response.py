from typing import Any, Generic, TypeVar

from pydantic import BaseModel

# 泛型数据载体：data 的类型随每个接口变化（如 BookOut、List[BookOut]）
DataT = TypeVar("DataT")


class ApiResponse(BaseModel, Generic[DataT]):
    # 业务码：0 成功，非 0 失败；与 HTTP 状态码解耦，方便前端统一判断
    code: int = 0
    msg: str = "success"
    data: DataT | None = None


def success(data: Any = None, msg: str = "success") -> ApiResponse:
    # 成功：code 固定 0
    return ApiResponse(code=0, msg=msg, data=data)


def fail(code: int = 1, msg: str = "请求失败", data: Any = None) -> ApiResponse:
    # 失败：code 为业务错误码
    return ApiResponse(code=code, msg=msg, data=data)

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    total: int
    page: int
    page_size: int
    data: list[T]
