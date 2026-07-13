from pydantic import BaseModel
import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client

security = HTTPBearer()


class Task(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None
    created_at: str | None = None
    
    