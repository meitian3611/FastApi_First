class ApiError(Exception):
    # 业务异常：在 service / router 里 raise，由 main.py 的全局处理器
    # 统一转成 {code, msg, data} 响应体，避免散落的 try/except
    def __init__(self, msg: str = "业务错误", code: int = 400, data=None):
        self.msg = msg
        self.code = code
        self.data = data
        super().__init__(msg)
