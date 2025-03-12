import boto3

# AWS S3 setup
s3_client = boto3.client("s3")
S3_BUCKET = "accounting-ai-project"


def get_s3_content_from_uri(s3_uri):
    # S3 uri example - s3://accounting-ai-project/uploads/accounting.txt
    # Remove the 's3://' prefix and split by the first '/'
    path_without_prefix = s3_uri[5:]
    parts = path_without_prefix.split('/', 1)

    object_key = parts[1] if len(parts) > 1 else ''

    # Fetch the content from S3
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=object_key)
        file_content = response['Body'].read().decode('utf-8')
        return file_content
    except Exception as e:
        raise Exception(f"Error fetching S3 content: {str(e)}")


async def upload_file_to_s3(file, file_content, file_path):
    # Upload to S3
    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=file_path,
        Body=file_content,
        ContentType=file.content_type
    )
    # Simulate s3 file path
    s3_url = f"s3://{S3_BUCKET}/{file_path}"
    return s3_url
