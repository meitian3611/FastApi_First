from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_serializer

"""
    自定义公共的基类 字段处理
"""
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True) # 允许直接读 ORM 模型对象来序列化

    @field_serializer("create_time", "update_time", check_fields=False)
    def serialize_datetime(self, value: datetime | None):
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")