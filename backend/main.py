"""FastAPI 入口：CORS、init_db、註冊所有路由。"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routers import auth, messages, profile, projects
from utils import ok

app = FastAPI(title="Portfolio API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/")
def root():
    return ok({"name": "Portfolio API", "version": "1.0.0"}, "API 運作中")


app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(messages.router)
app.include_router(profile.router)
