from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix='/api/tts', tags=['ai'])


@router.get('/synth/')
async def get_simple_llm_request(request: str):
    print('do something', request) 

    return {"word": request}