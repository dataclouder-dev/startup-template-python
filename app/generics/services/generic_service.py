from typing import Any
from bson import ObjectId

from dataclouder_core.models.models import FiltersConfig

from app.generics.models.generic_model import GenericModel
from app.generics.models.operation_dto import OperationDto
from app.generics.repositories import generic_repository


def save_generic(generic: GenericModel) -> Any:
    """Save generic using execute_operation."""
    generic_dict = generic.model_dump()
    
    if hasattr(generic, "id") and generic.id:
        query = {"_id": generic.id}
        generic_dict.pop("id", None)
    else:
        query = {"_id": str(ObjectId())}

    operation = OperationDto(action="findOneAndReplace", query=query, payload=generic_dict, options={"upsert": True})
    return generic_repository.execute_operation(operation)


def find_generics(generic_id: str) -> Any:
    """Find generic by id using execute_operation."""
    operation = OperationDto(action="findOne", query={"_id": generic_id})
    return generic_repository.execute_operation(operation)


def find_filtered_generics(filters: FiltersConfig) -> Any:
    """Find filtered generics using execute_operation."""
    operation = OperationDto(action="find", query=filters.model_dump())
    return generic_repository.execute_operation(operation)


def delete_generic(generic_id: str) -> Any:
    """Delete generic using execute_operation."""
    operation = OperationDto(action="deleteOne", query={"_id": generic_id})
    return generic_repository.execute_operation(operation)


def execute_operation(operation: OperationDto, collection_name: str = "generic") -> Any:
    """Execute a generic operation."""
    return generic_repository.execute_operation(collection_name, operation)
