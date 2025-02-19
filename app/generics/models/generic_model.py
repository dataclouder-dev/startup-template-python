# Define schema
from typing import Literal

from pydantic import BaseModel


class GenericModel(BaseModel):
    id: str
    name: str
    description: str
    type: Literal["gen1", "gen2", "gen3"]
    relation: dict
    # created_at: datetime
    # updated_at: datetime
