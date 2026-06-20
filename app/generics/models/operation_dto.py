from typing import Any, Literal, Optional, Dict, List, Union

from pydantic import BaseModel, Field


class OperationDto(BaseModel):
    action: Literal[
        "findOne",
        "find",
        "create",
        "updateOne",
        "updateMany",
        "deleteOne",
        "deleteMany",
        "aggregate",
        "findOneAndReplace",
    ] = Field(..., description="The action to perform")
    
    query: Optional[Dict[str, Any]] = Field(
        None, description="The query to select documents"
    )
    
    payload: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = Field(
        None, description="The payload for create, update or aggregate operations"
    )
    
    projection: Optional[Dict[str, Any]] = Field(
        None, description="The projection for find operations"
    )
    
    options: Optional[Dict[str, Any]] = Field(
        None, description="Options for find operations (e.g., limit, sort)"
    )
