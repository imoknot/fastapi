from http import HTTPStatus
from random import random
from uuid import UUID

import bcrypt
from fastapi import HTTPException

from app.models.users import UserDB
from app.repositories.user import UserRepository
from app.schemes.users import User, UserChangePassword, UserCreate
from app.services.auth import AuthService


class UserService:
    def __init__(self):
        self.user_repository: UserRepository = UserRepository()

    def _generate_password_salt(self) -> str:
        return bcrypt.gensalt().decode('utf-8')

    async def create_or_update_user(self, user_data: UserCreate) -> User:
        user_dict = user_data.model_dump(exclude_none=True)

        if user_data.password:
            user_dict['password_salt'] = self._generate_password_salt()
            user_dict['password'] = AuthService.hash_password(user_data.password, user_dict['password_salt'])

        user_data = await self.user_repository.create_or_update_user(user_dict)
        return User(**user_data.__dict__)

    async def change_password(self, user_uuid: UUID, user_password_data: UserChangePassword) -> bool:
        user_dict: UserDB = await self.user_repository.get_user_by_uuid(user_uuid)

        current_password_hash = AuthService.hash_password(user_password_data.password, user_dict.password_salt)
        if user_dict.password != current_password_hash:
            raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail='Passwords do not match')

        password_salt = self._generate_password_salt()
        await self.user_repository.update_user(
            user_uuid,
            {
                'password': AuthService.hash_password(user_password_data.password_new, password_salt),
                'password_salt': password_salt,
            },
        )

        return True
