from dataclouder_core.exception import handler_exception
from dataclouder_core.models.models import FiltersConfig
from fastapi import APIRouter
from typing_extensions import Any

from app.generics.models.generic_model import GenericModel
from app.generics.services import generic_service

router = APIRouter(prefix="/api/generics", tags=["Generics"])


@router.get("/")
@handler_exception
async def get_generic() -> Any:
    return {"hi", "hello"}


@router.get("/{id}")
@handler_exception
async def get_generic_by_id(id: str):
    return {"id": id}


@router.post("/")
@handler_exception
async def save_generic(generic: GenericModel):
    generic = generic_service.save_generic(generic)
    return generic


@router.post("/query")
@handler_exception
async def find_filtered_generics(filters: FiltersConfig):
    print(filters)
    generic = generic_service.find_filtered_generics(filters)
    return generic
