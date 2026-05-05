// 前台共用：API_BASE、navbar 行動選單、GSAP 進場、reduced-motion
window.API_BASE = 'https://portfolio-1-iw4i.onrender.com';

document.addEventListener('DOMContentLoaded', () => {
  // 行動裝置漢堡選單
  const toggle = document.getElementById('navToggle');
  const mobile = document.getElementById('navMobile');
  toggle?.addEventListener('click', () => mobile?.classList.toggle('hidden'));

  // GSAP 全域動畫初始化
  if (window.gsap && window.ScrollTrigger) {
    gsap.registerPlugin(ScrollTrigger);

    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) {
      gsap.globalTimeline.timeScale(100);
      return;
    }

    gsap.utils.toArray('.fade-up').forEach((el) => {
      gsap.from(el, {
        scrollTrigger: { trigger: el, start: 'top 88%' },
        y: 40,
        opacity: 0,
        duration: 0.8,
        ease: 'power3.out',
      });
    });

    gsap.utils.toArray('.fade-stagger').forEach((parent) => {
      const children = parent.querySelectorAll(':scope > *');
      gsap.from(children, {
        scrollTrigger: { trigger: parent, start: 'top 85%' },
        y: 30,
        opacity: 0,
        duration: 0.7,
        ease: 'power3.out',
        stagger: 0.12,
      });
    });

    // 按鈕 hover 微互動
    document.querySelectorAll('.btn-anim').forEach((btn) => {
      btn.addEventListener('mouseenter', () => gsap.to(btn, { scale: 1.05, duration: 0.25, ease: 'power2.out' }));
      btn.addEventListener('mouseleave', () => gsap.to(btn, { scale: 1, duration: 0.25, ease: 'power2.out' }));
    });
  }
});

// 共用 fetch helper（公開端點用）
window.apiGet = async function (path) {
  try {
    const res = await fetch(window.API_BASE + path);
    return await res.json();
  } catch (e) {
    return { success: false, message: '連線失敗：' + e.message };
  }
};
window.apiPost = async function (path, body) {
  try {
    const res = await fetch(window.API_BASE + path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    return await res.json();
  } catch (e) {
    return { success: false, message: '連線失敗：' + e.message };
  }
};
