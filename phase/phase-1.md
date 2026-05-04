# Phase 1：後端基礎建設

## 這個階段在做什麼？

簡單說就是：**蓋好網站的「後廚房」。**

餐廳要開張，廚房得先裝好水電瓦斯。這個階段我們要把後端的核心建好：
- 資料庫（存資料的地方）
- 認證系統（登入/登出）
- API 入口（前端跟後端溝通的窗口）

完成後，你的後端就能跑起來，而且有一組管理員帳號可以登入了！

---

## 📋 Prompt（複製這段，貼到 Cursor Chat 送出）

```
請幫我建立後端的基礎架構，依照 fastapi.mdc 規範完成以下工作：

### 1. 資料庫模組 (backend/database.py)
- 用 Python 內建 sqlite3 連接 backend/portfolio.db
- 寫一個 init_db() 函式，啟動時自動建立以下資料表：
  - users（管理員帳號）：id, username, password_hash, created_at
  - projects（作品集）：id, title, description, tech_stack, image_url, demo_url, github_url, created_at
  - messages（訪客留言）：id, name, email, content, is_read, created_at
  - profile（個人資料）：id, name, title, bio, avatar_url, email, github, linkedin, updated_at
- 所有 SQL 用參數化查詢（? 佔位符）

### 2. 認證工具 (backend/auth_utils.py)
- 密碼雜湊：用 bcrypt
- JWT token：用 PyJWT，有效期 24 小時
- get_current_user() 函式：驗證 token，給受保護路由用

### 3. Pydantic Models (backend/models.py)
- 為每個資料表建立 Create 和 Response 的 schema
- 另外加 LoginRequest（username + password）和 TokenResponse

### 4. 主程式入口 (backend/main.py)
- FastAPI app + CORSMiddleware（允許所有來源）
- 啟動時呼叫 init_db()
- 先建一個測試用的根路由 GET / 回傳 { "success": true, "message": "API 運作中" }

### 5. 認證路由 (backend/routers/auth.py)
- POST /api/auth/login → 驗證帳密，回傳 JWT token
- POST /api/auth/init → 建立預設管理員帳號（admin / admin123）
- GET /api/auth/me → 回傳當前登入的使用者資訊（需認證）

### 6. 安裝相依套件
建立 backend/requirements.txt：
- fastapi
- uvicorn
- pyjwt
- bcrypt
- python-multipart

### 7. 自我驗證
完成後請幫我驗證：
1. 所有檔案都建立在正確位置（backend/ 下）
2. 執行 `cd backend && pip install -r requirements.txt && python -c "from database import init_db; init_db(); print('DB OK')"` 確認資料庫初始化成功
3. 執行 `cd backend && uvicorn main:app --reload --port 8000` 確認伺服器啟動
4. 呼叫 POST /api/auth/init 建立預設管理員
5. 呼叫 POST /api/auth/login 測試登入拿到 token
6. 所有 API 回傳格式都是 { "success": true/false, "data": ..., "message": "..." }
```

---

## ✅ 完成後的驗證清單

- [ ] `backend/database.py` 存在，4 張資料表建立成功
- [ ] `backend/auth_utils.py` 存在，bcrypt + JWT 正常
- [ ] `backend/models.py` 存在，所有 schema 完整
- [ ] `backend/main.py` 可以啟動（port 8000）
- [ ] `backend/routers/auth.py` 三個端點正常
- [ ] 預設管理員 admin / admin123 可以登入
- [ ] 拿到的 JWT token 格式正確
- [ ] API 回傳格式統一
