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


@router.get("/{generic_id}")
@handler_exception
async def get_generic_by_id(generic_id: str) -> dict:
    return generic_service.find_generics(generic_id)


@router.post("/")
@handler_exception
async def save_generic(generic: GenericModel) -> GenericModel:
    return generic_service.save_generic(generic)


@router.post("/query")
@handler_exception
async def find_filtered_generics(filters: FiltersConfig) -> list:
    print(filters)
    return generic_service.find_filtered_generics(filters)
