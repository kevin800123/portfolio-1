"""個人資料：取得 / 更新（單筆）。"""
from fastapi import APIRouter, Depends

from auth_utils import get_current_user
from database import get_db
from models import ProfileUpdate
from utils import ok

router = APIRouter(prefix="/api/profile", tags=["profile"])


DEFAULT_PROFILE = {
    "name": "Kevin",
    "title": "Full-Stack Developer",
    "bio": "熱愛打造優雅介面與穩定後端的全端工程師。",
    "avatar_url": None,
    "email": "kevin@example.com",
    "github": "https://github.com",
    "linkedin": "https://linkedin.com",
}


def _ensure_profile(conn) -> dict:
    row = conn.execute("SELECT * FROM profile WHERE id=1").fetchone()
    if row:
        return dict(row)
    conn.execute(
        "INSERT INTO profile (id, name, title, bio, avatar_url, email, github, linkedin) "
        "VALUES (1, ?, ?, ?, ?, ?, ?, ?)",
        (
            DEFAULT_PROFILE["name"],
            DEFAULT_PROFILE["title"],
            DEFAULT_PROFILE["bio"],
            DEFAULT_PROFILE["avatar_url"],
            DEFAULT_PROFILE["email"],
            DEFAULT_PROFILE["github"],
            DEFAULT_PROFILE["linkedin"],
        ),
    )
    conn.commit()
    return dict(conn.execute("SELECT * FROM profile WHERE id=1").fetchone())


@router.get("")
def get_profile():
    conn = get_db()
    data = _ensure_profile(conn)
    conn.close()
    return ok(data)


@router.put("")
def update_profile(p: ProfileUpdate, _: str = Depends(get_current_user)):
    conn = get_db()
    _ensure_profile(conn)
    conn.execute(
        "UPDATE profile SET name=?, title=?, bio=?, avatar_url=?, email=?, github=?, linkedin=?, "
        "updated_at=CURRENT_TIMESTAMP WHERE id=1",
        (p.name, p.title, p.bio, p.avatar_url, p.email, p.github, p.linkedin),
    )
    conn.commit()
    data = dict(conn.execute("SELECT * FROM profile WHERE id=1").fetchone())
    conn.close()
    return ok(data, "已更新")
