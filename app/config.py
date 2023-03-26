from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ML API"
    mysql_user: str
    mysql_root_password: str
    mysql_host: str
    mysql_database: str


settings = Settings()
