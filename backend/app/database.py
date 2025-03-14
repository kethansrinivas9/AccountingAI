import os

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend.helpers.env_helper import load_params_from_aws_ssm

dotenv.load_dotenv()
#Load the params from SSM if there are no values in .env file
load_params_from_aws_ssm()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       pool_size=5,  # Number of connections to keep open
                       max_overflow=10,  # Extra connections to allow temporarily
                       pool_recycle=300,  # Recycle connections after 5 minutes
                       pool_pre_ping=True  # Test connection before using it
                    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()