"""所有 Pydantic schema。"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# ---- Auth ----
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str


# ---- Projects ----
class ProjectBase(BaseModel):
    title: str
    description: str
    tech_stack: str
    image_url: Optional[str] = None
    demo_url: Optional[str] = None
    github_url: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int
    created_at: str


# ---- Messages ----
class MessageCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    email: str = Field(..., min_length=3, max_length=120)
    content: str = Field(..., min_length=1, max_length=2000)


class MessageUpdate(BaseModel):
    is_read: bool


class MessageResponse(BaseModel):
    id: int
    name: str
    email: str
    content: str
    is_read: bool
    created_at: str


# ---- Profile ----
class ProfileBase(BaseModel):
    name: str
    title: str
    bio: str
    avatar_url: Optional[str] = None
    email: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    id: int
    updated_at: str
