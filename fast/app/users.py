import uuid
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDMixin, models
from fastapi_users.authentication import (
    AuthenticationBackend, 
    BearerTransport,
    JWTStrategy, #JavaScript Web Token
)
from fastapi_users.db import SQLAlchemyUserDatabase
from app.db import User, get_user_db

SECRET = "GOUTLESSMAN-SECRET-KEY"  # Change this to a strong secret in production

class UserManager(UUIDMixin,BaseUserManager[User,uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
    

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db) 
    
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name = "jwt",
    transport = bearer_transport,
    get_strategy = get_jwt_strategy,
)
fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, auth_backend)
current_active_user = fastapi_users.current_user(active=True)