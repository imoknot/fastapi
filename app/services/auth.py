from datetime import datetime, timedelta
from http import HTTPStatus
from uuid import UUID

import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from app.repositories.user import UserRepository
from app.schemes.auth import Token, TokenData
from app.settings import settings

oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl='/v1/auth/login/')


class AuthService:
    def __init__(self):
        self.jwt_expire: int = settings.JWT_EXPIRES
        self.jwt_secret: str = settings.JWT_SECRET
        self.jwt_algorithm: str = settings.JWT_ALGORITHM
        self.uuid_version: int = 4
        self.user_repository: UserRepository = UserRepository()

    def create_token(self, user_uuid: UUID) -> Token:
        now = datetime.now()
        payload = {'exp': now + timedelta(seconds=self.jwt_expire), 'user_uuid': str(user_uuid)}
        token = jwt.encode(claims=payload, key=self.jwt_secret, algorithm=self.jwt_algorithm)
        return Token(access_token=token)

    @staticmethod
    def hash_password(password: str, password_salt: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), password_salt.encode('utf-8')).decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str, password_salt: str) -> bool:
        if self.hash_password(plain_password, password_salt) == hashed_password:
            return True
        else:
            return False

    async def authenticate_user(self, user_data: OAuth2PasswordRequestForm) -> Token:
        user_db = await self.user_repository.get_user_by_username(user_data.username.lower())
        if not user_db or not self.verify_password(user_data.password, user_db.password, user_db.password_salt):
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Incorrect username or password')
        return self.create_token(user_db.user_uuid)

    async def get_current_auth_user_data(self, token: str) -> TokenData:
        return TokenData(**self.decode_token(token))

    def decode_token(self, token: str) -> dict:
        try:
            payload: dict = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
        except JWTError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Could not validate credentials',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        return payload


async def checking_credentials(
    token: str = Depends(oauth2_scheme_user), auth_service: AuthService = Depends()
) -> TokenData:
    return await auth_service.get_current_auth_user_data(token)
