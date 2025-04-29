import os
import chromadb
import chromadb.config
from google import genai
from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions

load_dotenv()

eb_model = os.getenv("EMBEDDING_MODEL")

directory_path = "./data/text"

def load_documents_from_folder(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                documents.append({ "id" : filename, "text" : file.read()})
    return documents

def split_text(text, chunk_size=100, overlap=20):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        if chunk:
            chunks.append(chunk)
    return chunks

def gen_embedding(text):    
    embedding = model.encode(text)
    return embedding


# Load documents from the folder path
documents = load_documents_from_folder(directory_path)

chunk_documents = []
for doc in documents:
    chunks = split_text(doc["text"])
    for i, chunk in enumerate(chunks):
        chunk_documents.append({
            "id": f"{doc['id']}_{i}",
            "text": chunk
        })

print(f"Total chunks created: {len(chunk_documents)}")
print("Embedding using model:", eb_model)
# Initialize the embedding model
model = SentenceTransformer(eb_model)

texts = [chunk["text"] for chunk in chunk_documents]
ids = [chunk["id"] for chunk in chunk_documents]
embedding = model.encode(texts)

# Store the embeddings in ChromaDB
chroma_client = chromadb.PersistentClient(path="./data/chormadb")
collection = chroma_client.get_or_create_collection(name="document_embeddings")
collection.add(
    ids=ids,
    documents=texts,
    embeddings=embedding.tolist(),
)

print("Embeddings stored in ChromaDB.")
