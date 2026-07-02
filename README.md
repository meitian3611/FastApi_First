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
├── db.py               # 异步引擎 / Base / SessionLocal / get_db / create_table
├── main.py             # 应用入口：app 组装 + lifespan 建表
├── models/             # ORM 模型（每张表一个文件）
│   ├── __init__.py     #   集中引入所有模型 → import models 即触发注册
│   ├── books.py        #   Book 模型
│   └── user.py         #   User 模型
├── schemas/            # Pydantic 请求/响应模型
│   ├── __init__.py     #   集中引入
│   └── book_schemas.py #   BookCreate / BookOut
├── routers/            # 路由（按资源拆分）
│   ├── __init__.py     #   all_routers 列表，main 循环挂载
│   └── books_router.py #   /books 相关接口
├── pyproject.toml
├── uv.lock
├── .gitignore
└── test_main.http      # 接口请求示例
```

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

打开 `db.py`，把 `DATABASE_URL` 改成你自己的 MySQL 连接串：

```python
DATABASE_URL = "mysql+aiomysql://用户名:密码@地址:端口/库名"
```

> 默认值是 `mysql+aiomysql://root:123456@127.0.0.1:3306/FastApi`，仅适合本地练习。

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
- **按资源分层**：`models/` 放表结构，`schemas/` 放 Pydantic 模型，`routers/` 放接口。三个包的 `__init__.py` 各自集中引入 / 登记，新增资源只改对应 `__init__.py`，`main.py` 一行都不用动。


