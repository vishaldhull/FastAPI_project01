from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from typing import Annotated
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone


router = APIRouter()
SECRET_KEY = 'a0942cdd28e0e6526715ec450aba3a236014f951e052ec60188f607e6dd49f19'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserRequest(BaseModel):
    username: str
    first_name: str
    last_name: str
    password : str
    email: str
    role : str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(db, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta=timedelta):
    encode={'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    # Logic to create a user
    create_user_model = Users(
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        email=create_user_request.email,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )
    db.add(create_user_model)
    db.commit()
    return {"message": "User created successfully"}

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    # Logic for user login and token generation
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    
    return {"access_token": token, "token_type": "bearer"} 