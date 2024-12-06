### Crear conexiónes con Gemini. 

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

from app.llm import gemini_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix='/api/llm', tags=['ai'])


@router.get('/chat/')
async def get_simple_llm_request(request: str):
    print('do something', request) 
    model = gemini_service.GeminiLLM(model_name='models/gemini-1.5-flash')
    return model.complete(request)
    