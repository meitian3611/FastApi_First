from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 从 .env 读取；没配就用默认值（仅适合本地练习）
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # 数据库连接串（异步引擎 + aiomysql 驱动）
    database_url: str = "mysql+aiomysql://root:123456@127.0.0.1:3306/FastApi"
    # 是否打印 SQL 日志：本地调试开，上线关
    db_echo: bool = False


settings = Settings()
