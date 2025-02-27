### Crear conexiónes con Gemini.

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/api/image", tags=["ai"])


@router.get("/generate/")
async def get_simple_llm_request(request: str) -> dict:
    print("do something", request)

    return {"word": request}
