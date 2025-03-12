from datetime import datetime, timezone

from pgvector.sqlalchemy import VECTOR
from sqlalchemy import Column, Integer, String, DateTime

from backend.app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.now(timezone.utc))
    s3_url = Column(String, nullable=False)
    # This will store vector embeddings
    embedding = Column(VECTOR(1536), nullable=False)
