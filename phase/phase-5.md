# Phase 5：動畫與效能優化

## 這個階段在做什麼？

簡單說就是：**幫餐廳裝上霓虹燈和音樂，讓整體體驗再升級！**

功能都做好了，現在要讓網站的視覺效果更上一層樓：
- 強化 GSAP 滾動動畫
- 加入更多 hover 互動效果
- 效能優化（讓動畫不卡頓）
- 確保無障礙設計（respect 使用者的減少動畫偏好）

這個階段只動前台，後台維持原樣不碰！

---

## 📋 Prompt（複製這段，貼到 Cursor Chat 送出）

```
請依照 animation.mdc 規範，幫我強化所有前台頁面的動畫效果並做效能優化。

⚠️ 注意：只修改 frontend/ 下的前台頁面，不要動 frontend/admin/ 後台頁面！

### 1. 首頁 (index.html) 動畫強化
- Hero 區域加視差滾動效果（滾動時背景慢速移動）
- CTA 區塊滾動進場動畫
- 按鈕 hover 用 GSAP 做微放大效果（scale 1.1）

### 2. 關於我 (about.html) 動畫強化
- 大頭照進場時放大淡入（scale 0.8 → 1）
- 技能分類卡片 ScrollTrigger 依序出現（stagger 0.15）
- 經歷和學歷項目從左側滑入（x: -30）
- 卡片 hover 上移 + 發光陰影

### 3. 作品集 (projects.html) 動畫強化
- API 載入完成後觸發卡片進場動畫
- 載入前先清除舊的 ScrollTrigger
- 卡片 hover 上移 15px + cyan 發光陰影

### 4. 聯絡我 (contact.html) 動畫強化
- 表單欄位 focus 時 GSAP 邊框發光（cyan）
- 聯絡資訊卡片 ScrollTrigger 進場
- 送出按鈕點擊後有彈性回彈動畫（elastic ease）

### 5. CSS 效能優化
在所有前台頁面加入（或建立 frontend/css/performance.css）：
- GPU 加速：卡片加 will-change: transform, opacity
- 防止動畫抖動：backface-visibility: hidden
- 無障礙：@media (prefers-reduced-motion: reduce) 關閉所有動畫
- 圖片最佳化：img { width: 100%; height: auto; display: block }

### 6. RWD 最終檢查
確認所有頁面在三個斷點都正常：
- 手機（< 640px）：單欄排列
- 平板（640px - 1024px）：雙欄
- 桌面（> 1024px）：三欄
- 按鈕觸控目標至少 48x48px

### 7. 自我驗證
完成後請幫我驗證：
1. 所有前台頁面都有 ScrollTrigger 動畫
2. 動畫時長在 0.6 - 1.0 秒範圍
3. 只用 transform + opacity 做動畫（不動 width/height）
4. 沒有手動 addEventListener('scroll')，全用 ScrollTrigger
5. 後台頁面完全沒有 GSAP
6. prefers-reduced-motion 有生效
7. 手機版 RWD 正常
8. Console 沒有錯誤
```

---

## ✅ 完成後的驗證清單

- [ ] 首頁 Hero 視差效果正常
- [ ] 關於我大頭照 + 技能卡片動畫正常
- [ ] 作品集卡片進場 + hover 發光正常
- [ ] 聯絡頁 focus 發光 + 按鈕彈性動畫正常
- [ ] CSS 效能優化規則已加入
- [ ] `prefers-reduced-motion` 無障礙設計有效
- [ ] 三個斷點 RWD 正常
- [ ] 後台沒有被動到
- [ ] Console 沒有錯誤
