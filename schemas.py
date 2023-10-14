from pydantic import BaseModel
import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# class TokenCreate(BaseModel):
#     username:str
#     access_token:str
#     refresh_token:str
#     status:bool
#     created_date:datetime.datetime

# class TokenSchema(BaseModel):
#     access_token: str
#     refresh_token: str

# class TokenPayload(BaseModel):
#     sub: str = None
#     exp: int = None

class Token(BaseModel):
    access_token: str
    token_type: str

class UserData(BaseModel):
    username: str | None = None

class PostCreate(BaseModel):
    title: str
    content: str

class PostUpdate(BaseModel):
    title: str
    content: str