from typing import List
from fastapi import APIRouter , Depends, status, Response, HTTPException

from .. import schemas , database, models, oauth2
from sqlalchemy.orm import Session
from ..repository import blog

router = APIRouter(
    prefix="/blog",
    tags = ["Blogs"]
)

get_db = database.get_db


@router.get("/", response_model = List[schemas.ShowBlog])
def all(db : Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)


# creating new blog and set the status code
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.ShowBlog) 
def create(request : schemas.Blog,db : Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)): #created an instance for db
    return blog.create(request,db)

#deleting a particular blog where id == particular id
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def destroy(id,db:Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.destroy(id,db) 

#update a particular blog passing the request body schema of blog
@router.put("/{id}",status_code = status.HTTP_202_ACCEPTED)
def update(id,request:schemas.Blog,db:Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.update(id,request,db)
           

#show the particular blog with particular id
@router.get("/{id}",status_code = status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id,db : Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.show(id,db)
