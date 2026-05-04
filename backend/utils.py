"""統一回傳格式 helper。"""
from typing import Any
from fastapi import HTTPException


def ok(data: Any = None, message: str = "OK") -> dict:
    return {"success": True, "data": data, "message": message}


def fail(message: str, status_code: int = 400) -> None:
    raise HTTPException(
        status_code=status_code,
        detail={"success": False, "data": None, "message": message},
    )
