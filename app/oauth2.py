from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi. security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy import cast, String
from sqlalchemy.orm import Session
from typing import Annotated
from . import schemas, database, models
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")  
        id = str(id)

        if id is None:  
            raise credentials_exception 
        
        try:
            token_data = schemas.TokenData(id=id)
            return token_data 
        except ValidationError as exc:
            print(repr(exc.errors()[0]['type']))  
            print(exc)

    except JWTError:
        raise credentials_exception
    

    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"},)

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter((models.User.id) == token.id).first()
    return user
    