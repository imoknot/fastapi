from fastapi import APIRouter, Depends

from app.schemаs.users import UserChangePassword
from app.services.auth import checking_credentials
from app.services.users import UserService

router = APIRouter(prefix='/user', tags=['User'])


@router.post('/change_password/', response_model=bool)
async def change_password(
    user_password_data: UserChangePassword,
    auth_user: checking_credentials = Depends(),
    user_service: UserService = Depends(),
):
    return await user_service.change_password(auth_user.user_uuid, user_password_data)
