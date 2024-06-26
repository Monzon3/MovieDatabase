from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import functions.dbConnector as dbConnector
from jose import JWTError, jwt
from models.users import User, Token, TokenData
import os
from passlib.context import CryptContext
from typing import Optional


# to get a string like this run:
# openssl rand -hex 32 (can run this in Git bash, for example)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(username: str, password: str):
    """authenticate_user() receives username and password and verifies
    whether that 'username' is stored in the database and if that 'password' belongs to it.
    Since the passwords are not stored in plain text but their hashes, 
    the CryptContext's 'verify_password()' method is used.

    If the authentication succeeds, authenticate_user() returns the users's information."""
    
    user = dbConnector.get_user(username)
    if not user:
        return False

    # Check if the plain password introduced by the client and the hashed password stored in the database match
    if not crypt.verify(password, user['password']):
        return False
    else:
        return user


async def get_current_user(token: str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception
    
    user = dbConnector.get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(current_user: User=Depends(get_current_user)):
    if current_user['disabled']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail=f"User '{current_user['username']}' is disabled")
    return current_user


async def check_admin(current_user: User=Depends(get_current_active_user)):
    if current_user['user_rank'] != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Your User_rank must be 'admin' in order to perform this action.")
    return current_user


# Token-related methods
def generate_token(data: dict, expires_delta: Optional[timedelta]=None):
    """generate_token() is called from obtain_token() if the user is properly authenticated and 'enabled'."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def obtain_token(login_data):
    """obtain_token() will return a token if the provided user-password couple are in the database
    and the user is 'enabled'."""
    user = authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},)

    if user['disabled']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail=f"User '{user['username']}' is disabled")           

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generate_token(data={"sub": user['username']}, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")