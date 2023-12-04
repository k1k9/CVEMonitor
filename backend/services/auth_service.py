import os
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status


from models.user_model import User
from database import SessionLocal


SECRET = os.environ.get('SECRET') # openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(username: str, password: str):
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            return 444444
        
        if not pwd_context.verify(password, user.password):
            return 666666
        
        user.last_login = datetime.now()
        db.commit()
        db.refresh(user)
        
        return user
    except: pass
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception
    
    
def check_is_logged(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_token(token, credentials_exception)


def check_is_admin(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    username = verify_token(token, credentials_exception)
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user.permissions != 2:
            raise credentials_exception
    except:
        raise credentials_exception
    finally:
        db.close()
    return username