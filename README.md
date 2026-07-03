# FastAPI_First

FastAPI + 异步 SQLAlchemy 的入门练习项目。适合刚学 FastAPI 的同学对照着看：从异步引擎、依赖注入到路由分层，一步步是怎么搭起来的。

## 技术栈

- **Web 框架**：FastAPI
- **ORM**：SQLAlchemy 2.0（声明式 `Mapped` 风格）+ 异步引擎
- **数据库**：MySQL（异步驱动 `aiomysql`）
- **包管理**：`uv`（`pyproject.toml` + `uv.lock`），要求 Python ≥ 3.13
- **服务器**：uvicorn

## 目录结构

```
FastAPI_First/
├── app/                # 应用包（入口 + 组件）
│   ├── main.py         #   应用入口：app 组装 + lifespan 建表
│   ├── core/           # 基础设施
│   │   ├── config.py   #   pydantic-settings 配置
│   │   ├── db.py       #   异步引擎 / Base / SessionLocal / get_db / create_table
│   │   ├── response.py #   统一响应体 ApiResponse[DataT] + success()/fail()
│   │   ├── exceptions.py # 业务异常 ApiError
│   │   └── exception_handlers.py # 4 个全局异常处理器，register_exception_handlers(app) 挂载
│   ├── models/         # ORM 模型（每张表一个文件）
│   │   ├── __init__.py #   集中引入所有模型
│   │   ├── books.py    #   Book 模型
│   │   └── user.py     #   User 模型
│   ├── schemas/        # Pydantic 请求/响应模型
│   │   ├── __init__.py #   集中引入
│   │   └── book_schemas.py
│   ├── services/       # 业务逻辑层（DB 操作在此，router 只做校验与调用）
│   │   ├── __init__.py #   集中引入
│   │   └── books_service.py
│   └── routers/        # 路由（按资源拆分）
│       ├── __init__.py #   all_routers 列表，main 循环挂载
│       └── books_router.py
├── pyproject.toml
├── uv.lock
├── .env.example        # 配置样例
├── .gitignore
└── test_main.http      # 接口请求示例
```

## 统一响应与异常处理

所有接口对外都返回同一套结构，前端只按 `code` 判断成功与否：

```json
{ "code": 0, "msg": "success", "data": { ... } }
```

- `app/core/response.py`：`ApiResponse[DataT]` 是泛型响应体，`success(data)` / `fail(code, msg)` 是构造器；router 用 `response_model=ApiResponse[BookOut]` 这样的写法声明。
- `app/core/exceptions.py`：`ApiError` 是在 service / router 中 raise 的业务异常。
- `app/core/exception_handlers.py` 集中定义并注册 4 个全局异常处理器：`ApiError`、FastAPI 的 `HTTPException`、`RequestValidationError`（参数校验失败）、以及兜底的 `Exception`；`app/main.py` 只调一次 `register_exception_handlers(app)`。它们都会被转成上面的统一响应体，业务代码里不用再散落 `try/except`。

> 当前实现里 HTTP 状态码会随错误类型返回（如 422 / 500），`code` 字段与之保持一致。如果你们团队约定"无论成败都返回 HTTP 200，只用 `code` 区分"，把各处理器里的 `status_code` 改成 200 即可。

## 快速开始

### 1. 准备环境

- 本机安装 Python ≥ 3.13
- 本机运行一个 MySQL，并创建一个数据库（默认库名 `FastApi`）
- 安装 `uv`（https://docs.astral.sh/uv/）

### 2. 安装依赖

```bash
uv sync
```

这会根据 `uv.lock` 把依赖装进 `.venv/`。

### 3. 配置数据库连接

复制 `.env.example` 为 `.env`，按需修改：

```bash
cp .env.example .env
```

`.env` 内容：

```
DATABASE_URL=mysql+aiomysql://用户名:密码@地址:端口/库名
DB_ECHO=true   # 是否打印 SQL 日志，本地调试开，上线关
```

> 默认 `DATABASE_URL` 是 `mysql+aiomysql://root:123456@127.0.0.1:3306/FastApi`，仅适合本地练习；`DB_ECHO` 默认 `false`（不打印 SQL）。`.env` 已被 `.gitignore` 忽略，不会提交进仓库。

### 4. 启动服务

```bash
uv run uvicorn main:app --reload
```

启动后：

- 接口文档（Swagger UI）：http://127.0.0.1:8000/docs
- 根路由：http://127.0.0.1:8000/ 返回 `{"message": "Hello World"}`

应用启动时，`lifespan` 会自动执行 `create_table()`，为 `Base` 下所有模型建表。

## 接口一览

| 方法 | 路径 | 说明 |
|------|------|------|
| GET  | `/`        | 健康检查，返回 Hello World |
| GET  | `/books`   | 获取全部图书列表 |
| POST | `/books`   | 新增一本图书 |

POST `/books` 请求体示例：

```json
{
  "book_name": "Python 编程",
  "author": "张三",
  "price": 59.00,
  "publish_house": "某出版社"
}
```

## 设计要点（给初学者的说明）

- **异步 SQLAlchemy**：`create_async_engine` + `async_sessionmaker`，配合 `aiomysql` 异步驱动；处理函数用 `db: AsyncSession = Depends(get_db)` 注入会话。
- **时间字段用数据库侧默认值**：`server_default=text("CURRENT_TIMESTAMP")` / `server_onupdate=...`，保证任何写入方式（含批量更新）时间都会自动刷新。注意：时间由数据库计算，不会自动进 Python 对象，需 `await db.refresh(obj)` 才能读到。
- **按资源分层**：`models/` 放表结构，`schemas/` 放 Pydantic 模型，`services/` 放业务逻辑（DB 操作都在这层），`routers/` 只做参数校验与调用 service。四个包的 `__init__.py` 各自集中引入 / 登记，新增资源只改对应 `__init__.py`，`main.py` 一行都不用动。


