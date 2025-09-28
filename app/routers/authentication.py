
from .. import schemas ,database, models, token
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from ..hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/authentication",
    tags=["authentication"]
)

@router.post("/login")
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)): 
    user=db.query(models.User).filter(models.User.name == request.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="Invalid Creds")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=404, detail="incorrect pass") 

    access_token = token.create_access_token(data={"sub": user.name})

    return {"access_token":access_token, "token_type":"bearer"}


