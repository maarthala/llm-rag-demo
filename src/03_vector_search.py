import os
import chromadb
from google import genai
from google.genai import types
from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions

load_dotenv()

genai_api_key = os.getenv("GENAI_API_KEY")
eb_model = os.getenv("EMBEDDING_MODEL")
genai_model = os.getenv("GENAI_MODEL")
question = os.getenv("QUESTION")

gemini_client = genai.Client(
    api_key=genai_api_key,
    http_options=types.HttpOptions(api_version='v1beta'),
    )


model = SentenceTransformer(eb_model)

def gen_embedding(text):    
    embedding = model.encode(text)
    return embedding

def call_genai(question, relevent_chunks):
    context = "\n".join(relevent_chunks)
    prompt = f"""
    You are a helpful assistant. Answer the question based on the context provided.
    Context: {context}
    Question: {question}    
    Answer:
    """
    response = gemini_client.models.generate_content(
        model=genai_model,
        contents=prompt
    )
    return response

chroma_client = chromadb.PersistentClient(path="./data/chormadb")
collection = chroma_client.get_or_create_collection(name="document_embeddings")

query_embedding = gen_embedding(question)

results = collection.query(
    query_embeddings=[query_embedding],
    include=["documents", "metadatas"],
    n_results=5)

relevant_chunks = [doc for sublist in results["documents"] for doc in sublist]
ans = call_genai(question, relevant_chunks)
print(f"\n ### Question: {question} \n ##### Answer: {ans.text}")
