from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

from app.tts import google_tts

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/api/tts", tags=["ai"])


@router.get("/synth/")
async def get_simple_llm_request(request: str):
    print("do something ", request)

    data = google_tts.get_speech("  hello world can you hear me?", lang="en", is_ssml=False)
    return data
