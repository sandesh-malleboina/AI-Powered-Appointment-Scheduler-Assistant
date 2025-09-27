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

class DocumentResponse(DocumentBase):
    id: int
    content: Optional[str]
    summary: Optional[str]
    date: Optional[str]
    time: Optional[str]
    department: Optional[str]
    error_msg: Optional[str]

    class Config:
        from_attributes = True  # instead of orm_mode
