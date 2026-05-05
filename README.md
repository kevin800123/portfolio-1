# Portfolio · 個人履歷網站

> 一個全端的個人履歷網站，深色主題 + Glassmorphism + GSAP 動畫，搭配 FastAPI 後台管理系統。  
> 前端託管於 GitHub Pages，後端部署於 Render，資料庫使用 Supabase (PostgreSQL)。

**🌐 Live Demo → [kevin800123.github.io/portfolio-1](https://kevin800123.github.io/portfolio-1/)**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind-CDN-06B6D4?logo=tailwindcss&logoColor=white)
![GSAP](https://img.shields.io/badge/GSAP-3.12-88CE02?logo=greensock&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-4169E1?logo=postgresql&logoColor=white)
![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?logo=render&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## 🌐 線上連結

| 服務 | 網址 |
|------|------|
| **前端網站** | [kevin800123.github.io/portfolio-1](https://kevin800123.github.io/portfolio-1/) |
| **後端 API** | [portfolio-1-iw4i.onrender.com](https://portfolio-1-iw4i.onrender.com) |
| **API 互動文件** | [portfolio-1-iw4i.onrender.com/docs](https://portfolio-1-iw4i.onrender.com/docs) |

> **注意**：Render 免費方案有冷啟動機制，閒置 15 分鐘後首次請求可能需等待 20~30 秒。

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
- 安全：所有 SQL 參數化查詢 + Supabase RLS 已啟用
- 響應式：手機 / 平板 / 桌面三斷點
- 無障礙：自動偵測 `prefers-reduced-motion`
- 雙引擎：偵測 `DATABASE_URL` 自動切換 PostgreSQL / SQLite

---

## 🚀 快速啟動（本地開發）

### 1. 後端
```bash
cd backend
cp .env.example .env          # 編輯 .env 填入 DATABASE_URL（可選）
pip install -r requirements.txt
python seed.py                # 建立測試資料 + 預設管理員
uvicorn main:app --reload --port 8000
```

- API 根路由：http://localhost:8000
- 互動文件：http://localhost:8000/docs
- 預設管理員：`admin` / `admin123`

> 若 `.env` 內 `DATABASE_URL` 為空，後端自動使用 SQLite（`backend/portfolio.db`），不需要額外設定任何資料庫。

### 2. 前端
```bash
cd frontend
python -m http.server 8080
```
打開 http://localhost:8080。

### 3. 端對端測試
```bash
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
│   │   ├── fastapi.mdc             # 後端規範（DB / 認證 / API 格式）
│   │   ├── frontend.mdc            # 前端規範（顏色 / 卡片 / RWD）
│   │   └── animation.mdc           # GSAP 動畫規範（前台限定）
│   └── skills/                     # AI 編寫 SOP
│       ├── create-page/            # 前台頁面建立 SOP
│       ├── admin-page/             # 後台頁面建立 SOP
│       └── api-crud/               # CRUD API 建立 SOP
├── backend/
│   ├── main.py                     # FastAPI 入口 + CORS
│   ├── database.py                 # 雙引擎抽象（PG / SQLite 自動切換）
│   ├── auth_utils.py               # bcrypt + JWT
│   ├── models.py                   # Pydantic schema
│   ├── utils.py                    # 統一回傳 helper
│   ├── seed.py                     # 測試資料
│   ├── test_api.py                 # 端對端測試（15 項）
│   ├── requirements.txt
│   ├── Procfile                    # Render 啟動指令
│   ├── render.yaml                 # Render Blueprint 部署設定
│   ├── .env.example                # 環境變數樣板
│   └── routers/
│       ├── auth.py                 # 登入 / 初始化 / me
│       ├── projects.py             # 作品 CRUD
│       ├── messages.py             # 留言 CRUD + 統計
│       └── profile.py              # 個人資料
├── frontend/
│   ├── index.html                  # 首頁（Hero + 打字機 + 視差）
│   ├── projects.html               # 作品集（API 動態載入）
│   ├── about.html                  # 關於我（技能 + 時間軸）
│   ├── contact.html                # 聯絡我（表單 + 發光效果）
│   ├── login.html                  # 登入（JWT + 跳轉後台）
│   ├── css/performance.css         # GPU 加速 + 無障礙
│   ├── js/common.js                # 共用 fetch / 動畫初始化
│   └── admin/
│       ├── dashboard.html          # 儀表板（統計卡片）
│       ├── projects.html           # 作品 CRUD Modal
│       ├── messages.html           # 留言已讀 / 展開 / 刪除
│       ├── profile.html            # 個人資料表單
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
| 資料庫 | PostgreSQL (Supabase) / SQLite (本地) |
| 認證 | PyJWT + bcrypt |
| 前端部署 | GitHub Pages (`gh-pages` 分支) |
| 後端部署 | Render (Web Service) |
| 資料庫託管 | Supabase (Singapore) |

---

## ☁️ 部署架構

```
┌─────────────┐     HTTPS      ┌──────────────┐     PostgreSQL    ┌───────────┐
│  GitHub      │ ──────────────→│   Render      │ ───────────────→│ Supabase  │
│  Pages       │   API 呼叫     │  (FastAPI)    │   連線           │  (PG 15)  │
│  (前端)      │                │  (後端)       │                  │  (資料庫)  │
└─────────────┘                └──────────────┘                  └───────────┘
  gh-pages 分支                  main 分支/backend                 RLS 已啟用
```

### 資料庫（Supabase）
1. 到 [supabase.com](https://supabase.com) 建立專案
2. **Connect → Transaction pooler** 複製 Connection String（含密碼）
3. 啟用 RLS：SQL Editor 執行 `ALTER TABLE xxx ENABLE ROW LEVEL SECURITY`

### 後端（Render）
1. Render Dashboard → **New → Web Service** → 連結此 GitHub repo
2. **Root Directory**：`backend`
3. **Build Command**：`pip install -r requirements.txt`
4. **Start Command**：`uvicorn main:app --host 0.0.0.0 --port $PORT`
5. 環境變數：
   - `DATABASE_URL` = Supabase Transaction pooler 連線字串
   - `PORTFOLIO_SECRET` = 一串 32+ 字元的亂數
6. 部署完成後呼叫 `POST /api/auth/init` 建立管理員

### 前端（GitHub Pages）
- `gh-pages` 分支存放 `frontend/` 的所有檔案（扁平化至根目錄）
- Settings → Pages → Source: Deploy from `gh-pages` branch

### 資料庫引擎自動切換
- 有 `DATABASE_URL` → 連 PostgreSQL（雲端模式）
- 沒有 `DATABASE_URL` → 退回 SQLite（本地開發模式）

---

## 📜 授權

[MIT License](./LICENSE)
