from fastapi import APIRouter, HTTPException
from database import engine
from sqlmodel import Session, select
from .models import Borrower
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_409_CONFLICT
from repos.user_repos import select_all_users, select_user, find_user
from auth.auth import AuthHandler