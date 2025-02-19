from dataclouder_core.models.models import FiltersConfig

from app.generics.models.generic_model import GenericModel
from app.generics.repositories import generic_repository


def save_generic(generic: GenericModel) -> GenericModel:
    return generic_repository.save_generic(generic)


def find_filtered_generics(filters: FiltersConfig) -> GenericModel:
    return generic_repository.find_filtered_generics(filters)


def delete_generic(id: str) -> GenericModel:
    return generic_repository.delete_generic(id)
