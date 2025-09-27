# app/main.py
import os
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database, schemas
from .routers import results   # <-- import router
from ML import ocr, summarizer 



models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Register router
app.include_router(results.router)

# -----------------------------
# Background Processing Function
# -----------------------------
def process_file(doc_id: int, db_session: Session):
    doc = db_session.query(models.Document).get(doc_id)
    if not doc:
        return
    try:
        doc.status = "processing"
        db_session.commit()
        extracted_text = ocr.run_ocr(doc.filepath)
        summary_dict = summarizer.summarize_text(extracted_text)
        doc.content = extracted_text
        # doc.summary = summary_text
        doc.date = summary_dict.get("date")
        doc.time = summary_dict.get("time")
        doc.department = summary_dict.get("department")
        doc.status = "completed"
        doc.error_msg = None
        db_session.commit()
    except Exception as e:
        doc.status = "failed"
        doc.error_msg = str(e)
        db_session.commit()

@app.get("/")
def root():
    return {"message": "API is running"}


@app.post("/upload", response_model=schemas.DocumentResponse)
async def upload_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(database.get_db)
):
    allowed_ext = (".pdf", ".png", ".jpg", ".jpeg", ".txt")
    if not file.filename.lower().endswith(allowed_ext):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as f:
        f.write(await file.read())

    doc = models.Document(filename=file.filename, filepath=save_path, status="pending")
    db.add(doc)
    db.commit()
    db.refresh(doc)

    background_tasks.add_task(process_file, doc.id, db)
    return doc

@app.post("/retry/{doc_id}", response_model=schemas.DocumentResponse)
def retry_processing(doc_id: int, background_tasks: BackgroundTasks = None, db: Session = Depends(database.get_db)):
    doc = db.query(models.Document).get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    doc.status = "pending"
    doc.error_msg = None
    db.commit()

    background_tasks.add_task(process_file, doc.id, db)
    return doc
