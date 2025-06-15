import os

from dotenv import load_dotenv

load_dotenv()

from dataclouder_tts import tts_controller, whisper_controller
from dc_agent_cards.controllers import agent_controller
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.generics.controller import generic_controller
from app.image_gen import image_gen
from app.llm import llm_router
from app.tts import tts_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["transcription"],
)


app.include_router(tts_router.router)
app.include_router(image_gen.router)
app.include_router(llm_router.router)
app.include_router(agent_controller.router)
app.include_router(generic_controller.router)
app.include_router(tts_controller.router)
app.include_router(whisper_controller.router)


@app.get("/", response_class=HTMLResponse)
def read_root() -> str:
    return "<h1>welcome</h1> <br> <a href='/docs'>docs</a>"


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None) -> dict:
    return {"item_id": item_id, "q": q}


@app.get("/vars")
def read_vars() -> tuple[str, str]:
    print(os.getenv("ENV"))
    print(os.getenv("VERSION"))
    return os.getenv("ENV"), os.getenv("VERSION")
