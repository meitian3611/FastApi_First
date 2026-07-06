from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

"""
封装 分页查询的公共函数

"""


async def pageInit(
        db: AsyncSession,
        stmt,
        page: int = 1,
        page_size: int = 10,
):
    # 1. 计算 offset
    offset = (page - 1) * page_size

    # 2. 查询总数
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar()

    # 3. 查询数据
    data_stmt = stmt.offset(offset).limit(page_size)
    result = await db.execute(data_stmt)
    items = result.scalars().all()

    # 4. 返回统一结构
    return {
        "data": items,
        "total": total,
        "page": page,
        "page_size": page_size
    }
