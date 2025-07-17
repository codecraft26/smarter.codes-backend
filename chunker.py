from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
import math

model = SentenceTransformer("all-MiniLM-L6-v2")
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def chunk_text(text: str, max_tokens: int = 500):  # changed from 100 to 500
    # Tokenize the text
    tokens = tokenizer.encode(text, add_special_tokens=False)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)
    print(f"[DEBUG] Chunked {len(chunks)} chunks from input text of length {len(text)}")
    return [{"text": chunk, "embedding": model.encode(chunk).tolist()} for chunk in chunks]
