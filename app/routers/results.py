# app/routers/results.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database, schemas

router = APIRouter(
    prefix="/results",
    tags=["results"]
)

@router.get("/{doc_id}")
def get_results(doc_id: int, db: Session = Depends(database.get_db)):
    doc = db.query(models.Document).get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not doc.date or not doc.time or not doc.department:
        return {"message": "Ambiguous date/time or department"}

    return doc



@router.get("/", response_model=list[schemas.DocumentResponse])
def list_documents(db: Session = Depends(database.get_db)):
    docs = db.query(models.Document).all()
    return docs
