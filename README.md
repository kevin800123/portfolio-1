# Portfolio · 個人履歷網站

> 一個全端的個人履歷網站，深色主題 + Glassmorphism + GSAP 動畫，搭配 FastAPI 後台管理系統。

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind-CDN-06B6D4?logo=tailwindcss&logoColor=white)
![GSAP](https://img.shields.io/badge/GSAP-3.12-88CE02?logo=greensock&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## ✨ 特色

### 前台（5 頁）
- **首頁**：Hero 全螢幕、漸層大標題、打字機效果、視差捲動、API 載入精選作品
- **作品集**：API 動態載入、卡片 hover 發光、ScrollTrigger 進場動畫
- **關於我**：個人資料 API、技能卡片、經歷時間軸、學歷
- **聯絡我**：表單驗證 + focus 發光、送出寫入資料庫、彈性回彈動畫
- **登入頁**：Glassmorphism 卡片、JWT 存 localStorage、跳轉後台

### 後台（4 頁）
- **儀表板**：作品數、留言數、未讀統計
- **作品管理**：CRUD Modal、新增 / 編輯 / 刪除
- **留言管理**：未讀高亮、展開內容、標記已讀、刪除
- **個人資料**：表單即時同步到前台

### 全棧細節
- 統一回傳格式：`{ success, data, message }`
- 認證：bcrypt 密碼雜湊 + PyJWT 24h token
- 安全：所有 SQL 參數化查詢
- 響應式：手機 / 平板 / 桌面三斷點
- 無障礙：自動偵測 `prefers-reduced-motion`

---

## 🚀 快速啟動

### 1. 後端
```powershell
cd backend
pip install -r requirements.txt
python seed.py                       # 建立測試資料 + 預設管理員
uvicorn main:app --reload --port 8000
```

- API 根路由：http://localhost:8000
- 互動文件：http://localhost:8000/docs
- 預設管理員：`admin` / `admin123`

### 2. 前端
```powershell
cd frontend
python -m http.server 8080
```
打開 http://localhost:8080。

### 3. 端對端測試（後端跑起來後）
```powershell
cd backend
python test_api.py
# → 通過 15/15
```

---

## 📁 專案結構

```
portfolio-1/
├── .cursor/
│   ├── rules/                      # AI 編寫規範
│   │   ├── fastapi.mdc
│   │   ├── frontend.mdc
│   │   └── animation.mdc
│   └── skills/                     # AI 編寫 SOP
│       ├── create-page/
│       ├── admin-page/
│       └── api-crud/
├── backend/
│   ├── main.py                     # FastAPI 入口 + CORS
│   ├── database.py                 # sqlite3 連線 + init_db
│   ├── auth_utils.py               # bcrypt + JWT
│   ├── models.py                   # Pydantic schema
│   ├── utils.py                    # 統一回傳 helper
│   ├── seed.py                     # 測試資料
│   ├── test_api.py                 # 端對端測試
│   ├── requirements.txt
│   └── routers/
│       ├── auth.py                 # 登入 / 初始化 / me
│       ├── projects.py             # 作品 CRUD
│       ├── messages.py             # 留言 CRUD + 統計
│       └── profile.py              # 個人資料
├── frontend/
│   ├── index.html
│   ├── projects.html
│   ├── about.html
│   ├── contact.html
│   ├── login.html
│   ├── css/performance.css         # GPU 加速 + 無障礙
│   ├── js/common.js                # 共用 fetch / 動畫初始化
│   └── admin/
│       ├── dashboard.html
│       ├── projects.html
│       ├── messages.html
│       ├── profile.html
│       └── js/auth.js              # authFetch / checkAuth / toast
└── phase/                          # 6 階段需求文件
```

---

## 🔌 API 端點

| Method | Path | 認證 | 說明 |
|--------|------|------|------|
| GET    | `/`                       | 公開 | 健康檢查 |
| POST   | `/api/auth/init`          | 公開 | 建立預設管理員 |
| POST   | `/api/auth/login`         | 公開 | 登入取得 JWT |
| GET    | `/api/auth/me`            | 🔒    | 當前使用者 |
| GET    | `/api/projects`           | 公開 | 作品列表 |
| GET    | `/api/projects/{id}`      | 公開 | 單筆作品 |
| POST   | `/api/projects`           | 🔒    | 新增作品 |
| PUT    | `/api/projects/{id}`      | 🔒    | 更新作品 |
| DELETE | `/api/projects/{id}`      | 🔒    | 刪除作品 |
| GET    | `/api/messages`           | 🔒    | 留言列表 |
| GET    | `/api/messages/stats`     | 🔒    | 留言統計 |
| POST   | `/api/messages`           | 公開 | 訪客留言 |
| PUT    | `/api/messages/{id}`      | 🔒    | 標記已讀 |
| DELETE | `/api/messages/{id}`      | 🔒    | 刪除留言 |
| GET    | `/api/profile`            | 公開 | 個人資料 |
| PUT    | `/api/profile`            | 🔒    | 更新個人資料 |

---

## 🛠️ 技術棧

| 層級 | 技術 |
|------|------|
| 前端 | HTML5 + Tailwind CDN + 純 JavaScript |
| 動畫 | GSAP 3.12 + ScrollTrigger |
| 後端 | FastAPI + Uvicorn |
| 資料庫 | PostgreSQL（Supabase） / SQLite（本地開發） |
| 認證 | PyJWT + bcrypt |
| 部署 | Render + Supabase |

---

## ☁️ 部署（Render + Supabase）

### 資料庫（Supabase）
1. 到 [supabase.com](https://supabase.com) 建立專案
2. **Connect → Transaction pooler** 複製 Connection String（含密碼）
3. 建議啟用 RLS（SQL Editor 執行 `ALTER TABLE xxx ENABLE ROW LEVEL SECURITY`）

### 後端（Render）
1. Render Dashboard → **New → Web Service** → 連結此 GitHub repo
2. **Root Directory**：`backend`
3. **Build Command**：`pip install -r requirements.txt`
4. **Start Command**：`uvicorn main:app --host 0.0.0.0 --port $PORT`
5. 環境變數設定：
   - `DATABASE_URL` = Supabase Transaction pooler 連線字串
   - `PORTFOLIO_SECRET` = 一串 32+ 字元的亂數
6. 部署完成後呼叫 `POST /api/auth/init` 建立管理員

### 資料庫引擎自動切換
- 有 `DATABASE_URL` → 連 PostgreSQL（雲端模式）
- 沒有 `DATABASE_URL` → 退回 SQLite（本地開發模式）

---

## 📜 授權

[MIT License](./LICENSE)
