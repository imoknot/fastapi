from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemаs.auth import Token
from app.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=['Authorization'])


@router.post('/login/', response_model=Token)
async def user_login(
    auth_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),
):
    """credentials default: admin"""
    return await auth_service.authenticate_user(auth_data)
