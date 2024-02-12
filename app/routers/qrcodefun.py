import fastapi
import segno
import io
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db


router = fastapi.APIRouter(prefix="/qr", tags=["Qr-code"])
IMAGE_DIR = "images/"


@router.get("/", status_code=fastapi.status.HTTP_200_OK)
def create_qr(payload: str):
    qrcode = segno.make(payload)
    buff = io.BytesIO()
    qrcode.save(buff, kind="png", scale=8)
    buff.seek(0)
    return StreamingResponse(content=buff, media_type="image/png")
