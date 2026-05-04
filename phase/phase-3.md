# Phase 3：後台管理系統

## 這個階段在做什麼？

簡單說就是：**蓋好餐廳的「辦公室」，讓老闆可以管理一切。**

前台是給訪客看的（漂亮），後台是給你自己用的（實用）。這個階段要建立後台管理介面：
- 左邊有選單（Sidebar）
- 右邊是操作區
- 可以新增 / 編輯 / 刪除作品和留言
- 沒登入的人進不來（JWT 認證保護）

後台不需要花俏動畫，重點是好用！

---

## 📋 Prompt（複製這段，貼到 Cursor Chat 送出）

```
請依照 admin-page Skill 和 frontend.mdc 規範，幫我建立後台管理系統。

### 共同要求
- 所有後台頁面放在 frontend/admin/ 目錄
- 每頁載入時檢查 localStorage 的 JWT token，沒有就跳轉 login.html
- 不用 GSAP 動畫，只用基本 CSS hover
- 深色主題（bg-slate-900）
- 引入 Tailwind CDN（不需要 GSAP CDN）

### 共用模組 (frontend/admin/js/auth.js)
- authFetch() 函式：自動帶 Authorization: Bearer token 的 fetch 封裝
- checkAuth() 函式：檢查 token 是否存在，不存在跳轉登入頁
- logout() 函式：清除 token + 跳轉登入頁
- API_BASE = 'http://localhost:8000'
- Toast 通知函式：成功（綠色）/ 失敗（紅色），3 秒後自動消失

### 頁面 1：儀表板 (frontend/admin/dashboard.html)
- 頂部歡迎訊息
- 統計卡片：作品總數、留言總數、未讀留言數
- 資料從 API 動態取得

### 頁面 2：作品管理 (frontend/admin/projects.html)
- 作品列表表格（標題、技術、建立日期、操作按鈕）
- 「新增作品」按鈕 → 彈出 Modal
- 每行有「編輯」和「刪除」按鈕
- Modal 彈窗：新增和編輯共用同一個
- 刪除前要確認
- CRUD 操作完成後自動刷新列表 + 顯示 Toast

### 頁面 3：留言管理 (frontend/admin/messages.html)
- 留言列表表格（寄件人、Email、內容預覽、日期、狀態）
- 未讀留言高亮顯示
- 點擊可展開查看完整內容
- 可標記已讀 / 刪除
- 刪除前要確認

### 頁面 4：個人資料 (frontend/admin/profile.html)
- 表單：名字、職稱、自我介紹、頭像網址、Email、GitHub、LinkedIn
- 載入時自動填入現有資料
- 「儲存」按鈕更新資料
- 儲存成功顯示 Toast

### 統一 Sidebar 選單
- 左側固定寬度（w-64）深色背景
- 選單項目：儀表板、作品管理、留言管理、個人資料、登出
- 當前頁面高亮（左邊 cyan 框線 + 文字 cyan）
- 右側主內容區 ml-64

### 自我驗證
完成後請幫我驗證：
1. 4 個 HTML + 1 個 JS 檔案都在正確位置
2. 未登入時會跳轉到 login.html
3. Sidebar 選單連結正確
4. 當前頁面有高亮效果
5. Modal 開關正常
6. authFetch 有正確帶 token
7. Toast 通知顯示正常
8. Console 沒有錯誤
```

---

## ✅ 完成後的驗證清單

- [ ] `frontend/admin/dashboard.html` — 統計卡片正常顯示
- [ ] `frontend/admin/projects.html` — CRUD Modal 正常
- [ ] `frontend/admin/messages.html` — 已讀/未讀 + 刪除正常
- [ ] `frontend/admin/profile.html` — 表單載入 + 儲存正常
- [ ] `frontend/admin/js/auth.js` — authFetch + Toast 正常
- [ ] 未登入跳轉登入頁正常
- [ ] Sidebar 高亮正確
- [ ] 後台沒有 GSAP（純 CSS hover）
