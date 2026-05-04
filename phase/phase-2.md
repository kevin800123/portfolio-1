# Phase 2：前台頁面開發

## 這個階段在做什麼？

簡單說就是：**蓋好餐廳的「門面」，讓客人走進來會「哇！」的那種。**

這個階段要建立 5 個超精美的前台頁面。每一頁都要有：
- 深色主題 + Glassmorphism 玻璃質感卡片
- GSAP 滾動動畫（滑到才出現）
- 漸層色大標題 + 打字機效果
- 手機 / 平板 / 桌面都好看（RWD）

Cursor 會自動參考你的 `frontend.mdc`、`animation.mdc` 規範和 `create-page` Skill 來生成！

---

## 📋 Prompt（複製這段，貼到 Cursor Chat 送出）

```
請依照 create-page Skill 和 frontend.mdc、animation.mdc 規範，幫我建立以下 5 個前台頁面。

所有頁面的共同要求：
- 深色主題（bg-slate-900）
- 統一導覽列（固定頂部、半透明模糊背景、當前頁面 cyan 高亮、手機版漢堡選單）
- 統一 Footer（版權 + GitHub / LinkedIn 社群連結）
- 所有卡片用 glassmorphism 風格：bg-white/5 backdrop-blur-lg border border-white/10 rounded-xl
- GSAP + ScrollTrigger 滾動進場動畫
- Tailwind RWD（sm / md / lg 斷點）
- 引入 Tailwind CDN + GSAP CDN + ScrollTrigger CDN

### 頁面 1：首頁 (frontend/index.html)
- Hero 區域佔滿全螢幕（min-h-screen）
- 大標題用漸層色（from-cyan-400 to-violet-400）
- 職稱文字用打字機效果（逐字出現 + 閃爍游標 |）
- 背景有 CSS 漸層微動畫
- 精選作品區（3 張卡片，資料先寫死）
- CTA 按鈕引導到作品集頁

### 頁面 2：作品集 (frontend/projects.html)
- 頁面標題 + 簡短說明
- 作品卡片用 grid 排列（手機 1 欄、平板 2 欄、桌面 3 欄）
- 每張卡片：標題、描述、技術標籤、Demo / GitHub 連結
- 卡片 hover 發光上移效果
- 資料先寫死，Phase 4 再改成 API 動態載入

### 頁面 3：關於我 (frontend/about.html)
- 個人照片 + 自我介紹
- 技能列表（前端 / 後端 / 工具分類）
- 經歷時間軸
- 學歷區塊

### 頁面 4：聯絡我 (frontend/contact.html)
- 聯絡表單（姓名、Email、訊息內容）
- 表單欄位 focus 時有 cyan 發光效果
- 送出按鈕有動畫回饋
- 旁邊放聯絡資訊卡片（Email、GitHub、LinkedIn）
- 表單先做前端驗證，Phase 4 再串 API

### 頁面 5：登入頁 (frontend/login.html)
- 置中的登入卡片（glassmorphism 風格）
- 帳號 + 密碼輸入框
- 登入按鈕（hover 效果）
- 登入成功後存 token 到 localStorage，跳轉到後台 admin/dashboard.html
- 登入失敗顯示錯誤訊息
- API 串接：POST http://localhost:8000/api/auth/login

### 自我驗證
完成後請幫我驗證：
1. 5 個 HTML 檔案都在 frontend/ 目錄下
2. 每頁都有導覽列和 Footer
3. 首頁打字機效果正常運作
4. 所有卡片都是 glassmorphism 風格
5. GSAP 動畫（ScrollTrigger）正常觸發
6. 手機版 RWD 排版正確
7. 登入頁可以成功呼叫 API 並跳轉
8. Console 沒有錯誤（F12 檢查）
```

---

## ✅ 完成後的驗證清單

- [ ] `frontend/index.html` — Hero 全螢幕 + 打字機 + 漸層標題
- [ ] `frontend/projects.html` — 卡片 grid + hover 發光
- [ ] `frontend/about.html` — 技能 + 經歷時間軸
- [ ] `frontend/contact.html` — 表單 + focus 發光效果
- [ ] `frontend/login.html` — 登入功能 + 跳轉後台
- [ ] 所有頁面深色主題 + glassmorphism
- [ ] GSAP ScrollTrigger 動畫正常
- [ ] 手機 / 平板 / 桌面 RWD 正常
- [ ] 導覽列和 Footer 統一
