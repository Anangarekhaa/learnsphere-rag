# LearnSphere RAG Platform

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system for automatically answering vendor security questionnaires using uploaded reference documents.

The system allows users to:

- Sign up and log in
- Upload reference documents (3–8 documents)
- Upload a questionnaire document
- Automatically generate answers with citations
- Review and edit responses
- Export the completed questionnaire as a structured document

All answers are strictly grounded in the uploaded reference documents.  
If no relevant content is retrieved above the similarity threshold (0.40), or the answer cannot be grounded in the reference documents, the system returns:
Not found in references


---

## About LearnSphere (Fictional Company)

LearnSphere is a cloud-based Learning Management System (LMS) used by universities and professional training institutions.

The platform provides:

- Course hosting
- Assessments and grading
- Student progress tracking
- Secure assignment submission
- Identity provider (SSO) integration

LearnSphere stores student account data and academic records and aligns its internal controls with SOC 2 and ISO 27001 best practices.

---

## Reference Documents

The system uses internally created policy documents that act as the source of truth, including:

- Security Policy
- Infrastructure Overview
- Identity and Access Management
- Data Retention Policy
- Compliance and Vendor Management
- Service level Security Policy

These documents describe encryption practices, access control, MFA, vulnerability management, cloud hosting architecture, data retention rules, and compliance alignment.

---

## Tech Stack

### Backend
- FastAPI-based API
- PostgreSQL database
- SQLAlchemy ORM
- Sentence Transformers (`all-MiniLM-L6-v2`) for embeddings
- Cosine similarity retrieval
- Groq LLM (Llama 3.1 8B Instant) for answer generation
- JWT-based authentication

### Frontend
- React application
- TailwindCSS UI
- Editable answer interface
- Confidence visualization (High / Medium / Low)
- Document export workflow

---

## System Design

### 1. Reference Upload
Users upload one or multiple reference documents.

The system:
- Extracts text
- Splits into token-based chunks
- Generates normalized embeddings
- Stores embeddings in PostgreSQL
- Associates documents with the uploading user

Retrieval is filtered by `user_id`.

---

### 2. Questionnaire Processing
When a questionnaire is uploaded:

- The document is parsed into individual questions
- Each question is embedded
- Relevant chunks are retrieved using cosine similarity
- A similarity threshold (0.40) filters weak matches
- The LLM generates answers strictly from retrieved context
- Citations are attached

---

### 3. Confidence Strategy

Confidence is derived from:
- Top cosine similarity score
- Gap between top and second-best chunk
- Threshold validation

Confidence is categorized as:

- High
- Medium
- Low
- None (if unsupported)

---

### 4. Review & Export

Users can:
- Edit generated answers
- Save updates
- Export a `.docx` file

The exported document:
- Preserves original question order
- Keeps questions unchanged
- Inserts answers below each question
- Includes citations

---

## Assumptions Made

- Reference documents are well-structured policy documents.
- Uploaded files are primarily text-based (no advanced OCR).
- Users upload relevant documents before generating answers.
- Embedding search scale remains small.

---

## Trade-offs

### 1. No Dedicated Vector Database
Embeddings are stored in PostgreSQL using `FLOAT[]` arrays.
This simplifies infrastructure but would not scale efficiently for large datasets.

### 2. Basic Similarity Search
Cosine similarity is computed in application memory.
Not optimized for large-scale retrieval.

### 3. Threshold-Based Filtering
A fixed similarity threshold (0.40) is used.
It is not dynamically tuned per dataset.

### 4. No Re-ranking Model
There is no cross-encoder or advanced reranking step.

---

## Future Scope

1. Add vector indexing (e.g., pgvector or FAISS)
2. Introduce semantic re-ranking for better retrieval accuracy
3. Add evaluation metrics (precision / recall tracking)
4. Introduce role-based access controls
5. Improve confidence scoring calibration using score distribution analysis

---

## Author

Ananga Rekha B