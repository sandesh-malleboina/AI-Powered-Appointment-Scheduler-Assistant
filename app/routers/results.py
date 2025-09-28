# app/routers/results.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database, schemas
from .. import oauth2
router = APIRouter(
    prefix="/results",
    tags=["results"]
)



# @router.get("/all", response_model=list[schemas.DocumentResponse])
# def list_documents(current_user:schemas.TokenData = Depends(oauth2.get_current_user), db: Session = Depends(database.get_db)):
#     docs = db.query(models.Document).all()
#     return docs



@router.get("/all")
def get_user_documents(username:schemas.TokenData = Depends(oauth2.get_current_user), db: Session = Depends(database.get_db)):
    # Check if user exists
    user = db.query(models.User).filter(models.User.name == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get all documents for this user
    documents = db.query(models.Document).filter(models.Document.user_id == user.id).all()
    return [
        {
            doc
        }
        for doc in documents
    ]


@router.delete("/delete/{doc_id}", status_code=204)
def delete_document(
    doc_id: int,
    username: schemas.TokenData = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.name == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found or unauthorized")

    doc = db.query(models.Document).filter(
        models.Document.id == doc_id,
        models.Document.user_id == user.id
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found or not yours")

    db.delete(doc)
    db.commit()

    return {"message": f"Document {doc_id} deleted successfully"}

@router.get("/{doc_id}")
def get_results(
    doc_id: int,
    username: schemas.TokenData = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.name == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found or unauthorized")

    doc = db.query(models.Document).filter(
        models.Document.id == doc_id,
        models.Document.user_id == user.id   # ownership check
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found or not yours")

    if not doc.date or not doc.time or not doc.department:
        return {"message": "Ambiguous date/time or department"}

    if not doc.date or not doc.time or not doc.department:
        return {
            "status": "needs_clarification",
            "message": "Ambiguous date/time or department"
        }

    return doc

