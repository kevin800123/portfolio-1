// 後台共用：API_BASE、authFetch、checkAuth、logout、toast
window.API_BASE = 'https://portfolio-1-iw4i.onrender.com';

function checkAuth() {
  if (!localStorage.getItem('token')) {
    location.replace('../login.html');
  }
}

function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('username');
  location.replace('../login.html');
}

async function authFetch(url, options = {}) {
  const token = localStorage.getItem('token');
  const headers = { ...(options.headers || {}), Authorization: 'Bearer ' + token };
  if (options.body && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }
  const res = await fetch(url, { ...options, headers });
  if (res.status === 401) {
    logout();
    throw new Error('未授權');
  }
  return res;
}

function toast(message, type = 'success') {
  const wrap = document.getElementById('toast');
  if (!wrap) return alert(message);
  const colors = {
    success: 'bg-emerald-500/15 border-emerald-400/40 text-emerald-200',
    error:   'bg-rose-500/15 border-rose-400/40 text-rose-200',
    info:    'bg-cyan-500/15 border-cyan-400/40 text-cyan-200',
  };
  const el = document.createElement('div');
  el.className = `border rounded-lg px-4 py-3 text-sm shadow-lg backdrop-blur ${colors[type] || colors.info} translate-x-4 opacity-0 transition`;
  el.textContent = message;
  wrap.appendChild(el);
  requestAnimationFrame(() => {
    el.classList.remove('translate-x-4', 'opacity-0');
  });
  setTimeout(() => {
    el.classList.add('opacity-0', 'translate-x-4');
    setTimeout(() => el.remove(), 300);
  }, 3000);
}

window.checkAuth = checkAuth;
window.logout = logout;
window.authFetch = authFetch;
window.toast = toast;
