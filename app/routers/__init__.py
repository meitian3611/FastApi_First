# 集中登记所有 router：新增资源时，建好 routers/xxx.py 后在此登记一行即可
from .books_router import router as books_router

all_routers = [books_router]
__all__ = ["all_routers"]
