from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import ApiError
from app.core.response import ApiResponse

# 以下都是普通异步函数（不依赖 app 实例），由 register_exception_handlers 统一挂载


async def api_error_handler(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.code,
        content=ApiResponse(code=exc.code, msg=exc.msg, data=exc.data).model_dump(),
    )


async def http_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse(code=exc.status_code, msg=exc.detail, data=None).model_dump(),
    )


async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=ApiResponse(code=422, msg="参数校验失败", data=exc.errors()).model_dump(),
    )


async def unexpected_error_handler(request: Request, exc: Exception):
    # 生产环境此处应记日志；练习项目仅返回统一错误体
    return JSONResponse(
        status_code=500,
        content=ApiResponse(code=500, msg="服务器内部错误", data=None).model_dump(),
    )


def register_exception_handlers(app) -> None:
    # main.py 调用一次即可挂载全部处理器；新增异常类型在此登记一行
    app.add_exception_handler(ApiError, api_error_handler)
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, unexpected_error_handler)
