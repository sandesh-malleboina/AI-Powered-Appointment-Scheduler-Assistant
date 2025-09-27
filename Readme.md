# Medical Document OCR & Summarizer API

This project provides a FastAPI-based backend for uploading medical documents (images, PDFs), extracting text using OCR, and summarizing appointment details (date, time, department) using NLP.

## Setup Instructions

### 1. Clone the repository

```sh
git clone <your-repo-url>
cd plum
```

### 2. Install Python dependencies

Create a virtual environment (recommended):

```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install required packages:

```sh
pip install -r requirements.txt
```

Download the SpaCy transformer model:

```sh
python -m spacy download en_core_web_trf
```

### 3. Run the API server

```sh
uvicorn app.main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000).

---

## Architecture Overview

- **app/**: FastAPI application code
  - `main.py`: Entry point, API endpoints, background processing
  - `database.py`: SQLAlchemy setup
  - `models.py`: ORM models
  - `schemas.py`: Pydantic schemas
  - `routers/results.py`: Results listing and retrieval endpoints
- **ML/**: Machine learning modules
  - `ocr.py`: OCR extraction (using PaddleOCR)
  - `summarizer.py`: NLP-based summarization (using SpaCy, dateparser)
- **uploads/**: Uploaded files storage
- **app.db**: SQLite database

---

## API Usage Examples

### 1. Upload a Document

**Endpoint:** `POST /upload`

**Request:**
- Form-data with file field

```sh
curl -F "file=@uploads/sample.jpg" http://localhost:8000/upload
```

**Response:**
```json
{
  "id": 1,
  "filename": "sample.jpg",
  "filepath": "uploads/sample.jpg",
  "status": "pending",
  "content": null,
  "summary": null,
  "date": null,
  "time": null,
  "department": null,
  "error_msg": null
}
```

### 2. Get Results for a Document

**Endpoint:** `GET /results/{doc_id}`

```sh
curl http://localhost:8000/results/1
```

**Response:**
```json
{
  "id": 1,
  "filename": "sample.jpg",
  "filepath": "uploads/sample.jpg",
  "status": "completed",
  "content": "...extracted text...",
  "date": "2024-06-01",
  "time": "09:30",
  "department": "Cardiology",
  "error_msg": null
}
```

### 3. List All Documents

**Endpoint:** `GET /results/`

```sh
curl http://localhost:8000/results/
```

**Response:**  
List of document objects.

### 4. Retry Processing a Document

**Endpoint:** `POST /retry/{doc_id}`

```sh
curl -X POST http://localhost:8000/retry/1
```

---

## Notes

- Supported file types: `.pdf`, `.png`, `.jpg`, `.jpeg`, `.txt`
- OCR uses PaddleOCR; summarization uses SpaCy transformer model.
- Results include extracted appointment date, time, and department.

---

## License
None