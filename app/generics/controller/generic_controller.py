from dataclouder_core.exception import handler_exception
from dataclouder_core.models.models import FiltersConfig
from fastapi import APIRouter

from app.generics.models.generic_model import GenericModel
from app.generics.services import generic_service

router = APIRouter(prefix="/api/generics", tags=["Generics"])


@router.get("/")
@handler_exception
async def get_generic() -> dict:
    return {"hi", "hello"}


@router.get("/{id}")
@handler_exception
async def get_generic_by_id(id: str) -> dict:
    return {"id": id}


@router.post("/")
@handler_exception
async def save_generic(generic: GenericModel) -> GenericModel:
    generic = generic_service.save_generic(generic)
    return generic


@router.post("/query")
@handler_exception
async def find_filtered_generics(filters: FiltersConfig) -> list:
    print(filters)
    generic = generic_service.find_filtered_generics(filters)
    return generic
