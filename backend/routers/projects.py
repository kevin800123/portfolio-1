"""作品集 CRUD。"""
from fastapi import APIRouter, Depends

from auth_utils import get_current_user
from database import get_db
from models import ProjectCreate, ProjectUpdate
from utils import fail, ok

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("")
def list_projects():
    conn = get_db()
    rows = conn.execute("SELECT * FROM projects ORDER BY id DESC").fetchall()
    conn.close()
    return ok([dict(r) for r in rows])


@router.get("/{pid}")
def get_project(pid: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM projects WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not row:
        fail("找不到作品", 404)
    return ok(dict(row))


@router.post("")
def create_project(p: ProjectCreate, _: str = Depends(get_current_user)):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO projects (title, description, tech_stack, image_url, demo_url, github_url) "
        "VALUES (?, ?, ?, ?, ?, ?) RETURNING id",
        (p.title, p.description, p.tech_stack, p.image_url, p.demo_url, p.github_url),
    )
    new_id = cur.fetchone()["id"]
    conn.commit()
    row = conn.execute("SELECT * FROM projects WHERE id=?", (new_id,)).fetchone()
    conn.close()
    return ok(dict(row), "已新增作品")


@router.put("/{pid}")
def update_project(pid: int, p: ProjectUpdate, _: str = Depends(get_current_user)):
    conn = get_db()
    if not conn.execute("SELECT 1 FROM projects WHERE id=?", (pid,)).fetchone():
        conn.close()
        fail("找不到作品", 404)
    conn.execute(
        "UPDATE projects SET title=?, description=?, tech_stack=?, image_url=?, demo_url=?, github_url=? WHERE id=?",
        (p.title, p.description, p.tech_stack, p.image_url, p.demo_url, p.github_url, pid),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM projects WHERE id=?", (pid,)).fetchone()
    conn.close()
    return ok(dict(row), "已更新")


@router.delete("/{pid}")
def delete_project(pid: int, _: str = Depends(get_current_user)):
    conn = get_db()
    if not conn.execute("SELECT 1 FROM projects WHERE id=?", (pid,)).fetchone():
        conn.close()
        fail("找不到作品", 404)
    conn.execute("DELETE FROM projects WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    return ok(None, "已刪除")
