from typing import List
from fastapi import APIRouter , Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from ..hashing import Hash
from .. import schemas , database, models

get_db = database.get_db
router = APIRouter()


#creating a new user
@router.post("/user",response_model=schemas.ShowUser,status_code=status.HTTP_201_CREATED, tags = [ "users"])
def create_user(request : schemas.User,db : Session = Depends(get_db)):
    new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#show a particular user with particular id
@router.get("/user/{id}",status_code = status.HTTP_200_OK, response_model=schemas.ShowUser, tags = ["users"])
def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with the id {id} is not available")
    return user