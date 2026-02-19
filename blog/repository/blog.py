from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from .. import models, schemas
from ..database import get_db



def get_all(db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

def  create(request:schemas.Blog,db:Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id,db:Session =Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return

def update(id,request:schemas.Blog,db:Session = Depends(get_db)):
    blog =db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    blog.update(request.dict())
    db.commit()
    return  "updated successfully"

def show(id,db:Session = Depends(get_db)):
    #this is a filter (or say where) in sql and we are getting the fist blog not all the blogs
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail":f"Blog with the id {id} is not available"}
    return blog