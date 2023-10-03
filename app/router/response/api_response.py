from typing import Any
from dataclasses import dataclass
from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
    success: bool = Field(..., title="ステータス")
    data: Any = Field(..., title="レスポンスデータ")


def success(data: Any = None) -> ApiResponse:
    """ 成功時のレスポンスを返す """
    return ApiResponse(success=True,
                       data=data)
