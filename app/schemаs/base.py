from fastapi import Query
from pydantic import BaseModel, Field

from app.settings import settings



class Pagination(BaseModel):
    data: list = Field(description='data objects', examples=[{'ice_mc': 'la la la'}])
    total_items: int = Field(description='Total objects count', examples=[100])
    total_pages: int = Field(description='Total pages count', examples=[10])


class PaginationParams(BaseModel):
    page: int = Field(Query(settings.PAGINATION_PAGE, ge=1, description='Current page number'))
    page_size: int = Field(
        Query(settings.PAGINATION_PAGE_SIZE, ge=1, le=settings.PAGINATION_PAGE_SIZE_MAX, description='Page size')
    )
