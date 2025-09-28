
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database, schemas
from ..hashing import Hash
from .. import oauth2

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/create", response_model=schemas.UserResponse)
def create_user(request:schemas.UserCreate, db :Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(
        (models.User.name == request.name) | (models.User.email == request.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=404, detail="User with this name or email already exists")

    new_user=models.User(name=request.name, email=request.email, password=Hash.do_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/details")
def get_user(user_name:schemas.TokenData = Depends(oauth2.get_current_user), db: Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.name == user_name).first()

    if not user:
        raise HTTPException(status_code=404, detail="user doesnt exists")
    return user
    