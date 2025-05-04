from boto3 import client
from core.config import settings

class S3Service:
    def __init__(self):
        self.s3 = client(
            's3',
            aws_access_key_id=settings.AWS_KEY,
            aws_secret_access_key=settings.AWS_SECRET
        )
        
    async def upload(self, file_content, filename: str, user_id: int) -> str:
        key = f"users/{user_id}/{filename}"
        self.s3.put_object(
            Bucket=settings.AWS_BUCKET,
            Key=key,
            Body=file_content
        )
        return f"https://{settings.AWS_BUCKET}.s3.amazonaws.com/{key}"