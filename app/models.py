from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from app.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.now(timezone.utc))
    s3_url = Column(String, nullable=False)
    # This will store vector embeddings
    embedding = Column(ARRAY(Float), nullable=False)
