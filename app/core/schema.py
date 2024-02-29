from typing import Generic, Optional, TypeVar

from fastapi import status as http_status
from pydantic import BaseModel
from pydantic.generics import GenericModel


class Error(BaseModel):
    code: int
    message: str


DataT = TypeVar("DataT")


class ResponseSchema(GenericModel, Generic[DataT]):
    data: Optional[DataT] or None
    error: Optional[Error] or None

    def ok(self):
        return self

    def body(self, data):
        self.data = data
        return self
