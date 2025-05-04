import mimetypes
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from utils.s3 import S3FileProcessor


router = APIRouter(prefix="/main", tags=["main"])

@router.get('/storage/')
def get_file(key: str):
    print(key)
    file = S3FileProcessor('contents').download_file(key)
    media_type, _ = mimetypes.guess_type(key)
    if media_type is None:
        media_type = "application/octet-stream"
    return StreamingResponse(
        file,
        media_type=media_type,
        headers={"Content-Disposition": f'inline; filename="{key.split("/")[-1]}"'}
    )