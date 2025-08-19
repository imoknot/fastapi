from http.client import responses

from fastapi import APIRouter, Depends

from app.schemаs.base import PaginationParams, Pagination
from app.services.auth import checking_credentials

router = APIRouter(prefix='/test_rout', tags=['Test Data'])


@router.post('/create/', deprecated=True)
async def test_create(
    auth_user: checking_credentials = Depends(),
):
    """im ok, im not alcoholic"""
    return auth_user

@router.get('/pagination_example/')
async def pagination_example(
    item: PaginationParams = Depends(),
    auth_user: checking_credentials = Depends()
) -> Pagination:
    """pagination example"""
    return Pagination(
        data=[{"example":"ok"}],
        total_pages=1,
        total_items=1003
    )
