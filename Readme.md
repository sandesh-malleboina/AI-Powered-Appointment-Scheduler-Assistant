# Medical Document OCR & Summarizer API

This project is a FastAPI-based backend for uploading medical documents (images, PDFs, text), extracting text using OCR, and summarizing appointment details (date, time, department) using NLP.

## Features

- **User Authentication**: Secure login and user management.
- **Document Upload**: Upload medical documents (PDF, PNG, JPG, JPEG, TXT).
- **OCR Extraction**: Extracts text from uploaded documents using PaddleOCR.
- **Appointment Summarization**: Uses SpaCy transformer model and dateparser to extract and normalize appointment details.
- **Results Management**: View, list, and delete processed documents.
- **Background Processing**: OCR and summarization run in the background after upload.
- **SQLite Database**: Stores users and document metadata.

## Project Structure

```
plum/
├── app/
│   ├── main.py            # FastAPI entry point
│   ├── models.py          # SQLAlchemy ORM models
│   ├── database.py        # Database setup
│   ├── schemas.py         # Pydantic schemas
│   ├── hashing.py         # Password hashing
│   ├── oauth2.py          # OAuth2 authentication
│   ├── token.py           # JWT token creation/verification
│   └── routers/
│       ├── authentication.py  # Login endpoint
│       ├── users.py           # User creation/details
│       └── results.py         # Document results endpoints
├── ML/
│   ├── ocr.py             # OCR extraction (PaddleOCR)
│   └── summarizer.py      # NLP summarization (SpaCy, dateparser)
├── uploads/               # Uploaded files
├── app.db                 # SQLite database
├── requirements.txt       # Python dependencies
└── Readme.md              # Project documentation
```

## Setup Instructions

### 1. Clone the repository

```sh
git clone <your-repo-url>
cd plum
```

### 2. Create a virtual environment and install dependencies

```sh
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

### 3. Download SpaCy transformer model

```sh
python -m spacy download en_core_web_trf
```

### 4. Run the API server

```sh
uvicorn app.main:app --reload
```

API will be available at [http://localhost:8000](http://localhost:8000).

## API Endpoints

### Authentication

- `POST /authentication/login`  
  Login with username and password. Returns JWT token.

### Users

- `POST /users/create`  
  Create a new user.

- `GET /users/details`  
  Get details of the current user.

### Documents

- `POST /upload`  
  Upload a document (requires authentication).

- `GET /results/all`  
  List all documents for the current user.

- `GET /results/{doc_id}`  
  Get results for a specific document.

- `DELETE /results/delete/{doc_id}`  
  Delete a document.

- `POST /retry/{doc_id}`  
  Retry processing a failed document.

## Example Usage

**Upload a document:**

```sh
curl -X POST -H "Authorization: Bearer <token>" -F "file=@uploads/sample.jpg" http://localhost:8000/upload
```

**List documents:**

```sh
curl -H "Authorization: Bearer <token>" http://localhost:8000/results/all
```

**Get document result:**

```sh
curl -H "Authorization: Bearer <token>" http://localhost:8000/results/1
```

## Notes

- Supported file types: `.pdf`, `.png`, `.jpg`, `.jpeg`, `.txt`
- OCR uses PaddleOCR; summarization uses SpaCy transformer model.
- Results include extracted appointment date, time, and department.

## License

None