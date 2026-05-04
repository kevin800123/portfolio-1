"""認證相關路由：登入、初始化管理員、取得當前使用者。"""
from fastapi import APIRouter, Depends

from auth_utils import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from database import get_db
from models import LoginRequest
from utils import fail, ok

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/init")
def init_admin():
    """建立預設管理員 admin / admin123（若已存在則略過）。"""
    conn = get_db()
    row = conn.execute("SELECT 1 FROM users WHERE username=?", ("admin",)).fetchone()
    if row:
        conn.close()
        return ok(None, "管理員已存在")
    conn.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        ("admin", hash_password("admin123")),
    )
    conn.commit()
    conn.close()
    return ok({"username": "admin"}, "已建立預設管理員 admin / admin123")


@router.post("/login")
def login(payload: LoginRequest):
    conn = get_db()
    row = conn.execute(
        "SELECT id, username, password_hash FROM users WHERE username=?",
        (payload.username,),
    ).fetchone()
    conn.close()
    if not row or not verify_password(payload.password, row["password_hash"]):
        fail("帳號或密碼錯誤", 401)
    token = create_access_token(row["username"])
    return ok(
        {"access_token": token, "token_type": "bearer", "username": row["username"]},
        "登入成功",
    )


@router.get("/me")
def me(username: str = Depends(get_current_user)):
    conn = get_db()
    row = conn.execute(
        "SELECT id, username, created_at FROM users WHERE username=?",
        (username,),
    ).fetchone()
    conn.close()
    if not row:
        fail("使用者不存在", 404)
    return ok(dict(row))
