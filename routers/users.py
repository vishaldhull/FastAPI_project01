from fastapi import APIRouter, Depends, Path, HTTPException
import models
from models import Todos, Users
from typing import Annotated
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserVerification(BaseModel):
    password: str = Field(min_length=6, max_length=100)
    new_password: str = Field(min_length=6, max_length=100)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=404, detail="Error on password change")
    
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


@router.put("/phonenumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(
    user: user_dependency, 
    db: db_dependency, 
    phone_number: str
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
    return {"message": "Phone number updated successfully"}