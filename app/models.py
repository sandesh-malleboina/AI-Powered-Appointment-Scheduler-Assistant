# # app/models.py
# from sqlalchemy import Column, Integer, String, Text
# from .database import Base

# class Document(Base):
#     __tablename__ = "documents"

#     id = Column(Integer, primary_key=True, index=True)
#     filename = Column(String, index=True)
#     filepath = Column(String)
#     content = Column(Text, nullable=True)
#     summary = Column(Text, nullable=True)
#     status = Column(String, default="pending")  # pending/processing/completed/failed
#     error_msg = Column(Text, nullable=True)

    
# app/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    filepath = Column(String)
    content = Column(Text, nullable=True)      # full OCR text
    # summary = Column(Text, nullable=True)      # optional textual summary
    date = Column(String, nullable=True)       # extracted/normalized date
    time = Column(String, nullable=True)       # extracted/normalized time
    department = Column(String, nullable=True) # extracted department
    status = Column(String, default="pending")  # pending/processing/completed/failed
    error_msg = Column(Text, nullable=True)

    user_id = Column(Integer, ForeignKey("user.id"))

    # relationship back to user
    owner = relationship("User", back_populates="documents")

class User(Base):
    __tablename__ = "user"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email=Column(String)
    password=Column(String)
    documents = relationship("Document", back_populates="owner")