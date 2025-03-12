from langchain_openai import OpenAIEmbeddings
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.app.models import Document

# OpenAI Embeddings
embeddings_model = OpenAIEmbeddings()


async def extract_and_store_document_embeddings(file_content: bytes, file_name: str, s3_url: str, db: Session):

    file_content_in_text_format = file_content.decode("utf-8")

    embedding = embeddings_model.embed_documents([file_content_in_text_format])[0]  # Generate embedding

    new_doc = Document(filename=file_name, s3_url=s3_url, embedding=embedding)
    db.add(new_doc)
    db.commit() #commits the file to DB since we disabled auto-commit


async def extract_closest_documents_based_on_embeddings(query_embedding: list[float], db: Session):
    # Perform vector search in NeonDB using pgvector by usign cosine similarity
    query = text(
        """
        SELECT filename, s3_url, 1 - (embedding <=> :query_embedding) AS similarity
        FROM documents
        ORDER BY similarity DESC
        LIMIT 3;
        """
    )

    result = db.execute(query, {"query_embedding": f"{query_embedding}"})

    return result.fetchall()