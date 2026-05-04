---
name: create-page
description: 建立前台精美頁面 SOP — 深色主題、Glassmorphism、GSAP 動畫、RWD。當使用者要求「建立 / 新增前台頁面」時使用。
---

# Skill：建立前台頁面 SOP

## 適用情境
- 在 `frontend/` 下建立新的訪客前台頁面（首頁、作品集、關於、聯絡、登入…）
- **不適用**於 `frontend/admin/` 後台頁面（請改用 `admin-page` skill）

## 必要規範
- 遵循 `frontend.mdc` 設計系統（顏色 / 卡片 / 表單 / RWD）
- 動畫部份遵循 `animation.mdc`

## 標準步驟

### 1. 確認頁面架構
頁面分為 4 區塊：
1. `<head>`：CDN 引入 + meta + title
2. Navbar（共用結構）
3. Main 內容（依頁面而異）
4. Footer + GSAP 初始化 script

### 2. HTML 樣板
```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>頁面標題 | Kevin Portfolio</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>
  <link rel="stylesheet" href="css/performance.css">
  <style>
    body { font-family: 'Inter', -apple-system, sans-serif; }
    .grad-text { background: linear-gradient(90deg,#22d3ee,#a78bfa); -webkit-background-clip:text; background-clip:text; color:transparent; }
    @keyframes blink { 50% { opacity: 0 } }
    .cursor-blink::after { content:'|'; animation: blink 1s step-end infinite; color:#22d3ee; }
  </style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen">
  <!-- Navbar -->
  <!-- Main -->
  <!-- Footer -->
  <script>gsap.registerPlugin(ScrollTrigger);</script>
</body>
</html>
```

### 3. Navbar（每頁複製，修改 active）
```html
<nav class="fixed top-0 inset-x-0 z-50 bg-slate-900/70 backdrop-blur-md border-b border-white/5">
  <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
    <a href="index.html" class="text-xl font-bold grad-text">Kevin.dev</a>
    <button id="navToggle" class="md:hidden text-slate-300" aria-label="選單">☰</button>
    <div id="navMenu" class="hidden md:flex gap-6 text-sm">
      <a href="index.html"    class="hover:text-cyan-400">首頁</a>
      <a href="projects.html" class="hover:text-cyan-400">作品集</a>
      <a href="about.html"    class="hover:text-cyan-400">關於我</a>
      <a href="contact.html"  class="hover:text-cyan-400">聯絡我</a>
      <a href="login.html"    class="hover:text-cyan-400">登入</a>
    </div>
  </div>
  <div id="navMobile" class="md:hidden hidden border-t border-white/5 px-6 py-4 flex-col gap-3 bg-slate-900/95"></div>
</nav>
<script>
  const t = document.getElementById('navToggle');
  const m = document.getElementById('navMobile');
  t?.addEventListener('click', () => m.classList.toggle('hidden'));
</script>
```
**將當前頁面那個 `<a>` 加上 `text-cyan-400 font-semibold`。**

### 4. Footer（每頁固定）
```html
<footer class="border-t border-white/5 mt-24 py-10 text-center text-slate-400 text-sm">
  <div class="flex justify-center gap-6 mb-4">
    <a href="https://github.com" class="hover:text-cyan-400">GitHub</a>
    <a href="https://linkedin.com" class="hover:text-cyan-400">LinkedIn</a>
  </div>
  <p>© 2026 Kevin Portfolio. All rights reserved.</p>
</footer>
```

### 5. GSAP 滾動動畫初始化
頁面底部固定加：
```html
<script>
  gsap.registerPlugin(ScrollTrigger);
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
    gsap.globalTimeline.timeScale(100);
  }
  gsap.utils.toArray('.fade-up').forEach(el => {
    gsap.from(el, {
      scrollTrigger: { trigger: el, start: 'top 85%' },
      y: 40, opacity: 0, duration: 0.8, ease: 'power3.out'
    });
  });
</script>
```

### 6. 自我驗證清單
- [ ] 頁面有 Navbar + 內容 + Footer
- [ ] 卡片是 glassmorphism 風格
- [ ] GSAP / ScrollTrigger 已引入並註冊
- [ ] 加入 `.fade-up` class 給要進場的元素
- [ ] RWD：手機 / 平板 / 桌面排版正常
- [ ] Console 無錯誤

## 常見錯誤
- ❌ 忘記 `gsap.registerPlugin(ScrollTrigger)` 導致 ScrollTrigger 不動
- ❌ 卡片用實色背景而非半透明（失去玻璃感）
- ❌ Mobile menu 沒寫 toggle
- ❌ 漸層文字漏 `bg-clip-text text-transparent`
