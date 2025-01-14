from dotenv import load_dotenv
load_dotenv() 

from fastapi import FastAPI


import os

from app.llm import llm_router
from app.tts import tts_router
from app.image_gen import image_gen
from app.modules.mongo import mongo_controller

from fastapi.responses import HTMLResponse


from app.tts import tts_router


app = FastAPI()

app.include_router(tts_router.router)
app.include_router(image_gen.router)
app.include_router(llm_router.router)
app.include_router(mongo_controller.router)


@app.get("/", response_class=HTMLResponse)
def read_root():
    return "<h1>welcome</h1> <br> <a href='/docs'>docs</a>"

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/vars")
def read_item():
    return showVariable()


def showVariable():
    print(os.getenv('ENV'))
    print(os.getenv('VERSION'))

    return os.getenv('ENV'), os.getenv('VERSION')
