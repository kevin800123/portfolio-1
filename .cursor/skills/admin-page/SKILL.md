---
name: admin-page
description: 建立後台管理頁面 SOP — Sidebar 佈局、JWT 保護、CRUD Modal、Toast 通知。當使用者要求建立 / 修改 frontend/admin/ 後台頁面時使用。
---

# Skill：建立後台管理頁面 SOP

## 適用情境
- 在 `frontend/admin/` 下建立後台管理頁面
- 必須有 JWT 認證保護
- **不使用 GSAP**，純 CSS hover

## 標準步驟

### 1. 頁面架構
```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>儀表板 | 後台</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="js/auth.js"></script>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen">
  <!-- Sidebar -->
  <!-- Main 內容 ml-64 -->
  <!-- Toast 容器 -->
  <script>checkAuth();</script>
  <script>/* 頁面 JS */</script>
</body>
</html>
```

### 2. 統一 Sidebar（每個後台頁面複製、修改 active）
```html
<aside class="fixed inset-y-0 left-0 w-64 bg-slate-950 border-r border-white/5 p-6 flex flex-col">
  <h1 class="text-xl font-bold mb-8">⚙️ 後台管理</h1>
  <nav class="flex flex-col gap-1 text-sm flex-1">
    <a href="dashboard.html" class="px-3 py-2 rounded hover:bg-white/5">📊 儀表板</a>
    <a href="projects.html"  class="px-3 py-2 rounded hover:bg-white/5">💼 作品管理</a>
    <a href="messages.html"  class="px-3 py-2 rounded hover:bg-white/5">✉️ 留言管理</a>
    <a href="profile.html"   class="px-3 py-2 rounded hover:bg-white/5">👤 個人資料</a>
  </nav>
  <button onclick="logout()" class="text-left px-3 py-2 rounded text-rose-300 hover:bg-rose-500/10">🚪 登出</button>
</aside>
<main class="ml-64 p-8"><!-- 內容 --></main>
<div id="toast" class="fixed top-6 right-6 z-50 space-y-2"></div>
```

當前頁面對應的 `<a>` 加上：`bg-cyan-500/10 text-cyan-400 border-l-2 border-cyan-400`

### 3. js/auth.js 共用模組（必備）
- `API_BASE`
- `checkAuth()`：讀 localStorage，無 token 跳 `../login.html`
- `authFetch(url, opts)`：自動 `Authorization: Bearer ${token}`
- `logout()`：清 token + 跳 `../login.html`
- `toast(msg, type)`：right-top 滑入，3 秒自動消失

### 4. CRUD Modal 樣板
```html
<div id="modal" class="fixed inset-0 z-40 hidden bg-black/60 flex items-center justify-center p-4">
  <div class="bg-slate-800 border border-white/10 rounded-xl w-full max-w-lg p-6">
    <h3 id="modalTitle" class="text-lg font-bold mb-4">新增作品</h3>
    <form id="modalForm" class="space-y-3">...</form>
    <div class="flex justify-end gap-2 mt-4">
      <button onclick="closeModal()" class="px-4 py-2 rounded bg-white/5">取消</button>
      <button onclick="saveItem()" class="px-4 py-2 rounded bg-cyan-500 hover:bg-cyan-400">儲存</button>
    </div>
  </div>
</div>
```

JS：
```js
function openModal(item) {
  // 填入資料 / 清空
  document.getElementById('modal').classList.remove('hidden');
}
function closeModal() {
  document.getElementById('modal').classList.add('hidden');
}
```

### 5. 表格樣板
```html
<table class="w-full text-sm">
  <thead class="text-left text-slate-400 border-b border-white/10">
    <tr><th class="py-3">標題</th>...<th>操作</th></tr>
  </thead>
  <tbody id="tbody"></tbody>
</table>
```

### 6. 標準 CRUD 流程
```js
async function loadList() {
  const res = await authFetch(`${API_BASE}/api/projects`);
  const json = await res.json();
  if (!json.success) return toast(json.message, 'error');
  render(json.data);
}
async function saveItem() {
  const data = collectForm();
  const isEdit = !!editingId;
  const res = await authFetch(
    `${API_BASE}/api/projects${isEdit ? '/' + editingId : ''}`,
    { method: isEdit ? 'PUT' : 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }
  );
  const json = await res.json();
  if (json.success) { toast('已儲存'); closeModal(); loadList(); }
  else toast(json.message, 'error');
}
async function deleteItem(id) {
  if (!confirm('確定刪除？')) return;
  const res = await authFetch(`${API_BASE}/api/projects/${id}`, { method: 'DELETE' });
  const json = await res.json();
  if (json.success) { toast('已刪除'); loadList(); }
}
```

### 7. 自我驗證
- [ ] Sidebar 連結正確、當前頁高亮
- [ ] 沒登入會跳 `../login.html`
- [ ] CRUD 新增 / 編輯 / 刪除全部正常
- [ ] Toast 顯示 3 秒消失
- [ ] 沒有 GSAP / ScrollTrigger
- [ ] Console 無錯誤
