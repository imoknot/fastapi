from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEVELOP: bool = False
    SERVER_HOST: str = '127.0.0.1'
    SERVER_PORT: int = 8989
    TITLE: str = 'API'
    VERSION: str = 'v1.0'
    DOC_URL: str = '/docs'
    OPENAPI_URL: str = '/openapi.json'
    LOG_LEVEL: str = 'debug'

    PAGINATION_PAGE: int = 1
    PAGINATION_PAGE_SIZE: int = 25
    PAGINATION_PAGE_SIZE_MAX: int = 100

    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5454
    POSTGRES_DB: str = 'project_pg_db'
    POSTGRES_USER: str = 'project_pg_user'
    POSTGRES_PASSWORD: str = 'project_pg_pass'

    POSTGRES_POOL_SIZE: int = 20
    POSTGRES_MAX_OVERFLOW: int = 5

    JWT_EXPIRES: int = 6000000000
    JWT_SECRET: str = 'GrandmaLivedWithTwoCheerfulGeeseOneGrayAndTheOtherWhiteTwoCheerfulGeese'
    JWT_ALGORITHM: str = 'HS256'

    WORKERS: int = 1


settings = Settings()
