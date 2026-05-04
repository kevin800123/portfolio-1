---
name: api-crud
description: 建立 FastAPI CRUD 路由 SOP — sqlite3、Pydantic、JWT 保護、統一回傳格式。當使用者要求建立後端 CRUD API 時使用。
---

# Skill：FastAPI CRUD API SOP

## 適用情境
- 在 `backend/routers/` 下建立資源型 CRUD 路由（projects、messages、profile…）
- 必須遵循 `fastapi.mdc` 規範

## 統一回傳格式
**任何端點都回 `{ "success": bool, "data": any, "message": str }`**

提供共用 helper：
```python
def ok(data=None, message="OK"):
    return {"success": True, "data": data, "message": message}

def fail(message: str, status_code: int = 400):
    raise HTTPException(status_code=status_code, detail={"success": False, "data": None, "message": message})
```

## 標準步驟

### 1. 在 `models.py` 新增該資源的 schema
```python
class ProjectBase(BaseModel):
    title: str
    description: str
    tech_stack: str
    image_url: Optional[str] = None
    demo_url: Optional[str] = None
    github_url: Optional[str] = None

class ProjectCreate(ProjectBase): pass
class ProjectUpdate(ProjectBase): pass
class ProjectResponse(ProjectBase):
    id: int
    created_at: str
```

### 2. 在 `database.py` 確保 table 已建立
（init_db 中已包含）

### 3. 建立 router 檔案 `backend/routers/<resource>.py`
模板：
```python
from fastapi import APIRouter, Depends
from typing import List
from database import get_db
from auth_utils import get_current_user
from models import ProjectCreate, ProjectUpdate, ProjectResponse
from utils import ok, fail   # 或在每個 router 內定義

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
    if not row: fail("找不到作品", 404)
    return ok(dict(row))

@router.post("")
def create_project(p: ProjectCreate, user=Depends(get_current_user)):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO projects(title, description, tech_stack, image_url, demo_url, github_url) VALUES (?,?,?,?,?,?)",
        (p.title, p.description, p.tech_stack, p.image_url, p.demo_url, p.github_url)
    )
    conn.commit()
    new_id = cur.lastrowid
    row = conn.execute("SELECT * FROM projects WHERE id=?", (new_id,)).fetchone()
    conn.close()
    return ok(dict(row), "已新增")

@router.put("/{pid}")
def update_project(pid: int, p: ProjectUpdate, user=Depends(get_current_user)):
    conn = get_db()
    if not conn.execute("SELECT 1 FROM projects WHERE id=?", (pid,)).fetchone():
        conn.close(); fail("找不到作品", 404)
    conn.execute(
        "UPDATE projects SET title=?, description=?, tech_stack=?, image_url=?, demo_url=?, github_url=? WHERE id=?",
        (p.title, p.description, p.tech_stack, p.image_url, p.demo_url, p.github_url, pid)
    )
    conn.commit()
    row = conn.execute("SELECT * FROM projects WHERE id=?", (pid,)).fetchone()
    conn.close()
    return ok(dict(row), "已更新")

@router.delete("/{pid}")
def delete_project(pid: int, user=Depends(get_current_user)):
    conn = get_db()
    if not conn.execute("SELECT 1 FROM projects WHERE id=?", (pid,)).fetchone():
        conn.close(); fail("找不到作品", 404)
    conn.execute("DELETE FROM projects WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    return ok(None, "已刪除")
```

### 4. 在 `main.py` 註冊
```python
from routers import auth, projects, messages, profile
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(messages.router)
app.include_router(profile.router)
```

### 5. 認證規則
- 公開：GET 列表 / GET 單筆 / 訪客 POST 留言 / GET profile
- 受保護：POST / PUT / DELETE / 留言列表 / 更新 profile
- 受保護端點透過 `user=Depends(get_current_user)` 帶入

### 6. SQL 安全
- ✅ 一律參數化查詢 `?`
- ❌ 禁止 f-string / `%s` 拼接

### 7. 自我驗證
- [ ] 公開端點不需 token 可存取
- [ ] 受保護端點沒 token 回 401
- [ ] 全部回傳 `{success, data, message}`
- [ ] 所有 SQL 用 `?` 參數化
- [ ] FastAPI `/docs` 看得到端點且能執行

## 常見錯誤
- ❌ 忘記 `conn.commit()` 導致變更沒寫入
- ❌ 忘記 `conn.close()` 造成連線洩漏
- ❌ 直接 return rows 給前端（要先 `dict(row)`）
