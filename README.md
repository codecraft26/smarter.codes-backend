# Smarter Code Backend & Frontend

## Overview
This project consists of a semantic search application with a React/Next.js frontend and a Python backend. It uses a vector database for efficient semantic search over HTML content.

---

## Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn
- (Optional) Docker (for containerized setup)

---

## Backend Setup
1. **Install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Run the backend server:**
   ```bash
   python main.py
   ```
   The backend will start on `http://127.0.0.1:8000` by default.

---

## Frontend Setup
1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   # or
   yarn install
   ```
2. **Configure API URL:**
   - Create a `.env.local` file in the `frontend` directory:
     ```env
     NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
     ```
3. **Run the frontend:**
   ```bash
   npm run dev
   # or
   yarn dev
   ```
   The frontend will start on `http://localhost:3000` by default.

---

## Vector Database Setup
- The backend uses a vector store (see `vector_store.py`).
- No external vector DB is required; it uses in-memory or file-based storage.
- For production, you may integrate with Pinecone, Weaviate, or similar (see comments in `vector_store.py`).

---

## Additional Notes
- Ensure both backend and frontend are running for full functionality.
- For Docker, see `docker-compose.yml` (if provided).

---

## Project Structure

```
smarter.code-backend/
├── main.py           # FastAPI app entry point, API endpoints
├── models.py         # Data models and Pydantic schemas
├── vector_store.py   # Vector database logic and integration
├── scraper.py        # HTML scraping and extraction utilities
├── chunker.py        # Text chunking and tokenization logic
├── docker-compose.yml# Docker Compose setup for backend and Weaviate
├── frontend/         # Next.js frontend application
│   ├── src/app/      # Main app directory (Next.js app router)
│   │   ├── components/   # Reusable UI components (Card, Input, etc.)
│   │   ├── page.tsx      # Main page, search UI logic
│   │   ├── layout.tsx    # App layout and global styles
│   │   └── globals.css   # Global CSS (Tailwind)
│   ├── public/       # Static assets (SVGs, images)
│   ├── package.json  # Frontend dependencies and scripts
│   └── ...           # Other config files
```

### Backend Files
- **main.py**: FastAPI app entry point, defines API endpoints for search and other operations.
- **models.py**: Contains Pydantic models and data schemas for request/response validation.
- **vector_store.py**: Handles all vector database logic, including integration with Weaviate or in-memory store.
- **scraper.py**: Utilities for scraping and extracting HTML content from URLs.
- **chunker.py**: Logic for splitting text into chunks and tokenizing for semantic search.

### Frontend Directory
- **frontend/src/app/components/**: Reusable React components (e.g., Card, Input) for UI consistency.
- **frontend/src/app/page.tsx**: Main search page, handles user input, API calls, and result rendering.
- **frontend/src/app/layout.tsx**: App-wide layout and theming.
- **frontend/src/app/globals.css**: Global styles, including Tailwind CSS setup.
- **frontend/public/**: Static files and images used in the UI.
- **frontend/package.json**: Lists frontend dependencies and scripts.

---

## Contact
For questions, contact [Your Name] or open an issue. 

---

## Running with Weaviate (Vector Database) via Docker Compose

**Step 1: Start Weaviate using Docker Compose**
- In the project root, ensure you have a `docker-compose.yml` file for Weaviate. Example:
  ```yaml
  version: '3.4'
  services:
    weaviate:
      image: semitechnologies/weaviate:1.24.10
      ports:
        - "8080:8080"
      environment:
        - QUERY_DEFAULTS_LIMIT=25
        - AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true
        - PERSISTENCE_DATA_PATH=/var/lib/weaviate
        - DEFAULT_VECTORIZER_MODULE=none
        - ENABLE_MODULES=none
      restart: on-failure
  ```
- Start Weaviate:
  ```bash
  docker-compose up -d
  ```
- Wait a few seconds for Weaviate to be ready at `http://localhost:8080`.

**Step 2: Start the Backend Server (Uvicorn)**
- In a new terminal, activate your Python environment and run:
  ```bash
  uvicorn main:app --reload
  ```
- The backend will start on `http://127.0.0.1:8000` by default.

**Step 3: Start the Frontend**
- In another terminal:
  ```bash
  cd frontend
  npm run dev
  ```
- The frontend will start on `http://localhost:3000` by default.

--- 