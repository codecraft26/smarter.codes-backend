# main.py
from fastapi import FastAPI
from models import SearchRequest, SearchResponse, ChunkResult
from scraper import fetch_and_clean_html
from chunker import chunk_text
from vector_store import store_chunks, search_query, delete_chunks_by_source

app = FastAPI(
    title="Semantic HTML Search API",
    description="Provide a URL and a query string to search the most relevant content chunks from that webpage.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI! Service is up."}


@app.post("/search", response_model=SearchResponse)
async def search_endpoint(request: SearchRequest):
    # Step 1: Fetch and clean HTML content from the provided URL
    html_text = fetch_and_clean_html(request.url)

    # Step 2: Tokenize and chunk the content into 500-token chunks
    chunks = chunk_text(html_text)

    # Step 2.5: Delete old chunks for this URL to avoid duplication
    delete_chunks_by_source(request.url)

    # Step 3: Store chunks and embeddings in Weaviate vector database, with source URL
    store_chunks(chunks, source=request.url)

    # Step 4: Search for relevant content based on the query (limit 10)
    search_results = search_query(request.query, source=request.url, limit=10)

    # Step 5: Build response with text and score
    results = [
        ChunkResult(html=item["html"], score=item["score"])
        for item in search_results
    ]

    return SearchResponse(results=results)
