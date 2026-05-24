# Resume Matcher

An AI-powered Resume-to-Job Matching API that analyzes a candidate’s resume against a job description and returns a semantic match score (0–100) along with an AI-generated explanation.

---

## Features

- Parse resumes in PDF, DOCX, and TXT formats
- Extract and preprocess resume content
- Semantic similarity matching between resume and job description
- Embedding-based retrieval using local Ollama models
- AI-generated explanation for match score
- Async FastAPI endpoints
- Structured JSON logging
- Rate limiting support
- Optional Langfuse observability/tracing
- Modular production-ready backend architecture

---

## Tech Stack

### Backend
- Python
- FastAPI

### AI / LLM
- Ollama
- LangChain
- llama3.2
- nomic-embed-text

### Observability
- Langfuse (Optional)

### Logging
- python-json-logger

---

## Project Structure

```bash
resume_matcher/
│
├── app/
│   ├── embedding/
│   │   ├── __init__.py
│   │   └── embedder.py
│   │
│   ├── matcher/
│   │   ├── __init__.py
│   │   └── matcher.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   │
│   ├── observability/
│   │   ├── __init__.py
│   │   └── langfuse_setup.py
│   │
│   ├── parser/
│   │   ├── __init__.py
│   │   └── resume_parser.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logging_config.py
│   │   └── rate_limiter.py
│   │
│   ├── config.py
│   └── main.py
│
├── data/
├── tests/
├── venv/
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Environment

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Pull Ollama Models

```bash
ollama pull nomic-embed-text
ollama pull llama3.2
```

### 5. Run FastAPI Server

```bash
uvicorn app.main:app --reload
```

### 6. Open API Docs

```bash
http://localhost:8000/docs
```

---

## API Endpoints

### POST `/match-single`

**Input**
- Resume file upload
- Job description text

**Output**
- Semantic match score (0–100)
- AI-generated explanation
- Structured JSON response

---

## Core Components

### Resume Parser
Extracts text from uploaded resume files (PDF, DOCX, TXT).

### Embedder
Converts resume and job description into vector embeddings using `nomic-embed-text`.

### Matcher
Calculates semantic similarity between resume and job description and generates explanation using LLM.

### Observability
Optional Langfuse integration for tracing and monitoring.

### Logging
Structured JSON logging using `python-json-logger`.

### Rate Limiter
Prevents API abuse and protects endpoints.

---

## Example Use Cases

- Resume Screening
- Candidate Matching
- ATS Pre-check
- HR Automation
- Job Fit Analysis

---

## Future Improvements

- Batch resume matching
- Rank multiple candidates
- Vector database integration (FAISS / ChromaDB)
- RAG-based hiring assistant
- Dashboard analytics
- ATS scoring enhancements

---

## Author

Built as part of an AI Engineering / LLM backend project using FastAPI, LangChain, Ollama, and local LLM workflows.