"""寫入測試資料。執行：python seed.py"""
from auth_utils import hash_password
from database import get_db, init_db


def seed():
    init_db()
    conn = get_db()

    if not conn.execute("SELECT 1 FROM users WHERE username='admin'").fetchone():
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            ("admin", hash_password("admin123")),
        )

    if not conn.execute("SELECT 1 FROM profile WHERE id=1").fetchone():
        conn.execute(
            "INSERT INTO profile (id, name, title, bio, avatar_url, email, github, linkedin) "
            "VALUES (1, ?, ?, ?, ?, ?, ?, ?)",
            (
                "Kevin Lin",
                "全端工程師 / UI 設計愛好者",
                "我是 Kevin，專注於 FastAPI 後端與精緻前端互動。喜歡把複雜的系統做得簡單好用。",
                "https://avatars.githubusercontent.com/u/1?v=4",
                "kevin@example.com",
                "https://github.com",
                "https://linkedin.com",
            ),
        )

    if conn.execute("SELECT COUNT(*) AS c FROM projects").fetchone()["c"] == 0:
        sample = [
            (
                "個人作品集網站",
                "使用 FastAPI + 純 HTML + Tailwind + GSAP 打造的全端作品集，包含後台管理系統。",
                "FastAPI,SQLite,Tailwind,GSAP",
                "https://picsum.photos/seed/portfolio/600/400",
                "https://example.com",
                "https://github.com",
            ),
            (
                "即時聊天室",
                "WebSocket 即時通訊應用，支援多房間與線上人數顯示。",
                "Python,WebSocket,Vue,Redis",
                "https://picsum.photos/seed/chat/600/400",
                "https://example.com",
                "https://github.com",
            ),
            (
                "電商後台儀表板",
                "可視化營收與訂單分析後台,包含圖表、訂單管理與權限控制。",
                "React,TypeScript,Node.js,PostgreSQL",
                "https://picsum.photos/seed/dash/600/400",
                "https://example.com",
                "https://github.com",
            ),
        ]
        conn.executemany(
            "INSERT INTO projects (title, description, tech_stack, image_url, demo_url, github_url) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            sample,
        )

    if conn.execute("SELECT COUNT(*) AS c FROM messages").fetchone()["c"] == 0:
        msgs = [
            ("Alice Wang", "alice@example.com", "你好，作品集做得很棒，想找你合作！"),
            ("Bob Chen", "bob@example.com", "請問有開放接案嗎？我們公司想做一個內部系統。"),
        ]
        conn.executemany(
            "INSERT INTO messages (name, email, content) VALUES (?, ?, ?)",
            msgs,
        )

    conn.commit()
    conn.close()
    print("[seed] 完成：admin/admin123、3 筆作品、2 筆留言、1 筆個人資料")


if __name__ == "__main__":
    seed()
