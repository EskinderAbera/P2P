from fastapi.security import HTTPBearer
from passlib.context import CryptContext
import datetime
from fastapi import Security, HTTPException

class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'])
    secret = 'supersecret'
    
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    def verify_password(self, pwd, hashed_pwd):
        return self.pwd_context.verify(pwd, hashed_pwd)