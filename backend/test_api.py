"""簡易端對端測試：對運行中的 API 打 7 個關鍵端點。"""
import io
import json
import sys
import urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE = "http://127.0.0.1:8000"


def req(method: str, path: str, body=None, token: str | None = None):
    url = BASE + path
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(r, timeout=5) as res:
            return res.status, json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, body


def main() -> None:
    failed = 0
    cases = []

    # 1. root
    s, j = req("GET", "/")
    cases.append(("GET /", s == 200 and j["success"]))

    # 2. login
    s, j = req("POST", "/api/auth/login", {"username": "admin", "password": "admin123"})
    ok_login = s == 200 and j["success"]
    cases.append(("POST /api/auth/login", ok_login))
    token = j["data"]["access_token"] if ok_login else None

    # 3. wrong password
    s, j = req("POST", "/api/auth/login", {"username": "admin", "password": "WRONG"})
    cases.append(("POST /api/auth/login (wrong pw → 401)", s == 401))

    # 4. me with token
    s, j = req("GET", "/api/auth/me", token=token)
    cases.append(("GET /api/auth/me", s == 200 and j["success"]))

    # 5. me without token
    s, j = req("GET", "/api/auth/me")
    cases.append(("GET /api/auth/me (no token → 401)", s == 401))

    # 6. list projects (public)
    s, j = req("GET", "/api/projects")
    cases.append(("GET /api/projects", s == 200 and j["success"] and isinstance(j["data"], list)))

    # 7. create project (auth)
    s, j = req(
        "POST",
        "/api/projects",
        {"title": "測試作品", "description": "from test", "tech_stack": "Python,FastAPI"},
        token=token,
    )
    ok_create = s == 200 and j["success"]
    cases.append(("POST /api/projects", ok_create))
    new_id = j["data"]["id"] if ok_create else None

    # 8. update project
    if new_id:
        s, j = req(
            "PUT",
            f"/api/projects/{new_id}",
            {"title": "測試作品-更新", "description": "updated", "tech_stack": "Python"},
            token=token,
        )
        cases.append(("PUT /api/projects/{id}", s == 200 and j["success"]))

        # 9. delete project
        s, j = req("DELETE", f"/api/projects/{new_id}", token=token)
        cases.append(("DELETE /api/projects/{id}", s == 200 and j["success"]))

    # 10. create message (public)
    s, j = req(
        "POST",
        "/api/messages",
        {"name": "tester", "email": "t@example.com", "content": "hi"},
    )
    cases.append(("POST /api/messages (public)", s == 200 and j["success"]))

    # 11. messages list (auth)
    s, j = req("GET", "/api/messages", token=token)
    cases.append(("GET /api/messages", s == 200 and j["success"]))

    # 12. messages stats
    s, j = req("GET", "/api/messages/stats", token=token)
    cases.append(("GET /api/messages/stats", s == 200 and j["success"] and "total" in j["data"]))

    # 13. profile public
    s, j = req("GET", "/api/profile")
    cases.append(("GET /api/profile (public)", s == 200 and j["success"]))

    # 14. profile update
    s, j = req(
        "PUT",
        "/api/profile",
        {"name": "Kevin", "title": "Dev", "bio": "test bio"},
        token=token,
    )
    cases.append(("PUT /api/profile", s == 200 and j["success"]))

    # 15. protected without token
    s, _ = req("DELETE", "/api/projects/1")
    cases.append(("DELETE /api/projects/1 (no token → 401)", s == 401))

    print("=" * 60)
    print(" API 端對端測試結果")
    print("=" * 60)
    for name, ok in cases:
        status = "✓ PASS" if ok else "✗ FAIL"
        if not ok:
            failed += 1
        print(f"  {status}  {name}")
    print("=" * 60)
    print(f" 通過 {len(cases) - failed}/{len(cases)}")
    raise SystemExit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
