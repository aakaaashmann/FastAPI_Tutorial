from typing import List
from fastapi import APIRouter , Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from ..hashing import Hash
from .. import schemas , database, models
from ..repository import user

get_db = database.get_db
router = APIRouter(
    prefix = "/user",
    tags =["Users"]

)


#creating a new user
@router.post("/",response_model=schemas.ShowUser,status_code=status.HTTP_201_CREATED)
def create_user(request : schemas.User,db : Session = Depends(get_db)):
    return user.create_user(request,db)


#show a particular user with particular id
@router.get("/{id}",status_code = status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id:int,db:Session = Depends(get_db)):
    return user.get_user(id,db)