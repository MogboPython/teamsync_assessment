from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class PostCreate(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True