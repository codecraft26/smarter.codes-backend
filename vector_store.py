import weaviate
import weaviate.classes as wvc
from weaviate.classes.query import Filter
from sentence_transformers import SentenceTransformer

# Create and connect client (Weaviate v4+)
client = weaviate.connect_to_local()

# Load the same model as used in chunker.py
model = SentenceTransformer("all-MiniLM-L6-v2")

def init_collection():
    if "HtmlChunk" not in client.collections.list_all():
        client.collections.create(
            name="HtmlChunk",
            properties=[
                wvc.config.Property(name="content", data_type=wvc.config.DataType.TEXT),
                wvc.config.Property(name="source", data_type=wvc.config.DataType.TEXT),
            ],
            vector_config=wvc.config.Configure.Vectors.self_provided()
        )

def store_chunks(chunks, source="unknown"):
    init_collection()
    collection = client.collections.get("HtmlChunk")
    print(f"[DEBUG] Storing {len(chunks)} chunks for source: {source}")
    for chunk in chunks:
        print(f"[DEBUG] Storing chunk text: {chunk['text'][:200]}")
        print(f"[DEBUG] Chunk vector length: {len(chunk['embedding'])}")
        collection.data.insert(
            properties={
                "content": chunk["text"],
                "source": source
            },
            vector=chunk["embedding"]
        )

def delete_chunks_by_source(source):
    init_collection()
    collection = client.collections.get("HtmlChunk")
    print(f"[DEBUG] Deleting chunks for source: {source}")
    # Use the correct filter object for property equality
    results = collection.query.fetch_objects(filters=Filter.by_property("source").equal(source), limit=1000)
    print(f"[DEBUG] Found {len(results.objects)} objects to delete for source: {source}")
    for obj in results.objects:
        collection.data.delete_by_id(obj.uuid)

def search_query(query, source=None, limit=5):
    init_collection()
    collection = client.collections.get("HtmlChunk")
    query_vector = model.encode(query).tolist()
    print(f"[DEBUG] Query vector length: {len(query_vector)}")
    print(f"[DEBUG] Searching for query: '{query}' with source: {source} and limit: {limit}")
    if source:
        results = collection.query.near_vector(
            query_vector,
            limit=limit,
            filters=Filter.by_property("source").equal(source),
            distance=1.0
        )
    else:
        results = collection.query.near_vector(query_vector, limit=limit, distance=1.0)
    print(f"[DEBUG] Found {len(results.objects)} search results")
    # BM25 fallback for debugging
    if len(results.objects) == 0:
        print("[DEBUG] Trying BM25 keyword search as fallback...")
        if source:
            bm25_results = collection.query.bm25(query=query, limit=limit, filters=Filter.by_property("source").equal(source))
        else:
            bm25_results = collection.query.bm25(query=query, limit=limit)
        print(f"[DEBUG] BM25 found {len(bm25_results.objects)} results")
        return [
            {"text": obj.properties["content"], "score": getattr(obj, 'score', 1.0)}
            for obj in bm25_results.objects
        ]
    return [
        {"text": obj.properties["content"], "score": obj.distance if hasattr(obj, 'distance') else 1.0}
        for obj in results.objects
    ]
