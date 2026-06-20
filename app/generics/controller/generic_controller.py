from dataclouder_core.exception import handler_exception
from dataclouder_core.models.models import FiltersConfig
from fastapi import APIRouter

from typing import Any

from app.generics.models.generic_model import GenericModel
from app.generics.models.operation_dto import OperationDto
from app.generics.services import generic_service

router = APIRouter(prefix="/api/generic", tags=["Generics"])


@router.get("/")
@handler_exception
async def get_generic():
    print("hi")
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


@router.post("/operation")
@handler_exception
async def execute_operation(operation: OperationDto) -> Any:
    """
    Execute a single database operation.
    Allows executing a variety of database operations through a single endpoint.
    Supported actions: 'findOne', 'find', 'create', 'updateOne', 'updateMany', 'deleteOne', 'deleteMany', 'aggregate'.
    """
    return generic_service.execute_operation(operation)
