import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from openai import OpenAI
import boto3

router = APIRouter(prefix="/documents", tags=["Documents"])
S3_BUCKET = "accounting-ai-project"

# AWS S3 setup
s3_client = boto3.client("s3")


@router.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    """Uploads document to S3 and processes it using AI"""
    file_path = f"uploads/{file.filename}"
    print("file path is: " + file_path)

    file_content = await file.read()

    # Upload to S3
    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=file_path,
        Body=file_content,
        ContentType=file.content_type
    )

    # Upload to S3
    s3_client.upload_file(file_path, S3_BUCKET, file.filename)

    return {"message": "File uploaded successfully", "filename": file.filename}
