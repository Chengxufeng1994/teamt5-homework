from typing import Generic, TypeVar

from pydantic import BaseModel


class OkResponse(BaseModel):
    message: str = 'OK'


class ErrorResponse(BaseModel):
    message: str
    error: str


# 定義泛型類型 T
T = TypeVar('T')


class GenericResponse(BaseModel, Generic[T]):
    message: str
    data: T | None = None  # data 是可選的，某些情況可能不回傳資料
