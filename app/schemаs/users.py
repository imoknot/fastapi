from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator


class UserPasswordSalt(BaseModel):
    password_salt: str | None = Field(examples=['Very Very RandomData'])


class UserPassword(BaseModel):
    password: str = Field(examples=['very secret password'])


class User(BaseModel):
    user_uuid: UUID | None = Field(None, examples=[uuid4()])
    username: str = Field(examples=['big_big_boss'])


class UserCreate(User, UserPassword):
    pass


class UserChangePassword(UserPassword):
    password_new: str = Field(examples=['New secret password'])

    @model_validator(mode='after')
    def check_abortion(self):
        if len(self.password_new) < 3:
            raise ValueError('New password must be at least 3 characters')
        if self.password == self.password_new:
            raise ValueError('passwords must not match')
        return self
