from pydantic import BaseModel, Field
from uuid import UUID


class Token(BaseModel):
    access_token: str = Field(example='LivedUgrandmotherThreeGeeseOneGreyOtherWhiteTwoFunnyGeese')


class TokenData(BaseModel):
    user_uuid: UUID = Field(examples=['00000000-0000-4000-0000-000000000001'])
