# # app/schemas.py
# from pydantic import BaseModel
# from typing import Optional

# class DocumentBase(BaseModel):
#     filename: str
#     filepath: str
#     status: str

# class DocumentResponse(DocumentBase):
#     id: int
#     content: Optional[str]
#     summary: Optional[str]
#     error_msg: Optional[str]

#     class Config:
#         from_attributes = True  # instead of orm_mode = True



# app/schemas.py
from pydantic import BaseModel
from typing import Optional

class DocumentBase(BaseModel):
    filename: str
    filepath: str
    status: str
    user_id:int

class DocumentResponse(DocumentBase):
    id: int
    content: Optional[str]
    date: Optional[str]
    time: Optional[str]
    department: Optional[str]
    error_msg: Optional[str]

    class Config:
        from_attributes = True  # instead of orm_mode
 


class User(BaseModel):
    name: str
    email: str

class UserCreate(User):
    password: str

class UserResponse(User):
    class Config:
        from_attributes = True  # allows ORM models to convert cleanly


class Login(BaseModel):
    username :str
    password:str

    class Config:
        from_attributes = True  # allows ORM models to convert cleanly

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None