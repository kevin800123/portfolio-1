"""訪客留言 CRUD + 統計。"""
from fastapi import APIRouter, Depends

from auth_utils import get_current_user
from database import get_db
from models import MessageCreate, MessageUpdate
from utils import fail, ok

router = APIRouter(prefix="/api/messages", tags=["messages"])


def _row_to_dict(row) -> dict:
    d = dict(row)
    d["is_read"] = bool(d.get("is_read", 0))
    return d


@router.get("/stats")
def stats(_: str = Depends(get_current_user)):
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) AS c FROM messages").fetchone()["c"]
    unread = conn.execute("SELECT COUNT(*) AS c FROM messages WHERE is_read=0").fetchone()["c"]
    conn.close()
    return ok({"total": total, "unread": unread})


@router.get("")
def list_messages(_: str = Depends(get_current_user)):
    conn = get_db()
    rows = conn.execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
    conn.close()
    return ok([_row_to_dict(r) for r in rows])


@router.get("/{mid}")
def get_message(mid: int, _: str = Depends(get_current_user)):
    conn = get_db()
    row = conn.execute("SELECT * FROM messages WHERE id=?", (mid,)).fetchone()
    conn.close()
    if not row:
        fail("找不到留言", 404)
    return ok(_row_to_dict(row))


@router.post("")
def create_message(m: MessageCreate):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO messages (name, email, content, is_read) VALUES (?, ?, ?, 0)",
        (m.name, m.email, m.content),
    )
    conn.commit()
    new_id = cur.lastrowid
    row = conn.execute("SELECT * FROM messages WHERE id=?", (new_id,)).fetchone()
    conn.close()
    return ok(_row_to_dict(row), "留言已送出，謝謝你！")


@router.put("/{mid}")
def update_message(mid: int, m: MessageUpdate, _: str = Depends(get_current_user)):
    conn = get_db()
    if not conn.execute("SELECT 1 FROM messages WHERE id=?", (mid,)).fetchone():
        conn.close()
        fail("找不到留言", 404)
    conn.execute(
        "UPDATE messages SET is_read=? WHERE id=?",
        (1 if m.is_read else 0, mid),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM messages WHERE id=?", (mid,)).fetchone()
    conn.close()
    return ok(_row_to_dict(row), "已更新")


@router.delete("/{mid}")
def delete_message(mid: int, _: str = Depends(get_current_user)):
    conn = get_db()
    if not conn.execute("SELECT 1 FROM messages WHERE id=?", (mid,)).fetchone():
        conn.close()
        fail("找不到留言", 404)
    conn.execute("DELETE FROM messages WHERE id=?", (mid,))
    conn.commit()
    conn.close()
    return ok(None, "已刪除")
