# Phase 4：前後端 API 串接

## 這個階段在做什麼？

簡單說就是：**把廚房和前台「接起來」，讓點菜單真的能送到廚房。**

前面我們分別蓋好了：
- 後端（Phase 1）→ 廚房
- 前台頁面（Phase 2）→ 餐廳門面
- 後台頁面（Phase 3）→ 辦公室

但目前它們還沒接上。這個階段要建立所有 CRUD API，讓前端的資料都能從後端動態讀取和修改。

---

## 📋 Prompt（複製這段，貼到 Cursor Chat 送出）

```
請依照 api-crud Skill 和 fastapi.mdc 規範，幫我建立所有 CRUD API 並串接前後端。

### 1. 作品集 API (backend/routers/projects.py)
用 api-crud Skill 的標準流程建立：
- GET /api/projects → 取得所有作品（公開）
- GET /api/projects/{id} → 取得單筆作品（公開）
- POST /api/projects → 新增作品（需認證）
- PUT /api/projects/{id} → 更新作品（需認證）
- DELETE /api/projects/{id} → 刪除作品（需認證）

### 2. 留言 API (backend/routers/messages.py)
- GET /api/messages → 取得所有留言（需認證）
- GET /api/messages/{id} → 取得單筆留言（需認證）
- POST /api/messages → 新增留言（公開，給訪客用）
- PUT /api/messages/{id} → 更新留言狀態，如標記已讀（需認證）
- DELETE /api/messages/{id} → 刪除留言（需認證）
- GET /api/messages/stats → 留言統計：總數 + 未讀數（需認證）

### 3. 個人資料 API (backend/routers/profile.py)
- GET /api/profile → 取得個人資料（公開）
- PUT /api/profile → 更新個人資料（需認證）

### 4. 在 main.py 註冊所有路由
把上面 3 個 router 都 include 進 main.py

### 5. 前台頁面串接
- frontend/projects.html → 改成呼叫 GET /api/projects 動態載入作品卡片
- frontend/index.html → 精選作品區改成呼叫 API 取最新 3 筆
- frontend/about.html → 呼叫 GET /api/profile 動態載入個人資料
- frontend/contact.html → 表單送出呼叫 POST /api/messages

### 6. 後台頁面串接
- admin/dashboard.html → 呼叫留言統計 API 顯示數據
- admin/projects.html → 完整 CRUD 串接（新增/編輯/刪除都呼叫 API）
- admin/messages.html → 串接留言 API（列表/已讀/刪除）
- admin/profile.html → 串接個人資料 API（讀取 + 更新）

### 7. 建立測試資料
建一個 backend/seed.py 腳本：
- 新增 3 筆範例作品（有中文標題和描述）
- 新增 2 筆範例留言
- 新增 1 筆個人資料
- 執行方式：python seed.py

### 8. 自我驗證
完成後請幫我驗證：
1. 所有 API 端點可以正常呼叫（用 curl 或 FastAPI /docs 測試）
2. 公開端點不需 token 就能存取
3. 受保護端點沒 token 會回 401
4. 前台頁面能正確顯示 API 回傳的資料
5. 後台 CRUD 操作（新增→編輯→刪除）完整流程正常
6. 所有 API 回傳格式統一：{ "success": true/false, "data": ..., "message": "..." }
7. 執行 seed.py 成功建立測試資料
8. Console 沒有錯誤
```

---

## ✅ 完成後的驗證清單

- [ ] `backend/routers/projects.py` — 5 個端點正常
- [ ] `backend/routers/messages.py` — 6 個端點正常
- [ ] `backend/routers/profile.py` — 2 個端點正常
- [ ] `main.py` 已註冊所有路由
- [ ] 前台動態載入資料正常
- [ ] 後台 CRUD 完整流程正常
- [ ] `backend/seed.py` 可執行 + 測試資料正確
- [ ] API 回傳格式統一
