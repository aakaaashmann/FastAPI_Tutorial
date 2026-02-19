from typing import List
from fastapi import APIRouter , Depends, status, Response, HTTPException

from .. import schemas , database, models
from sqlalchemy.orm import Session

router = APIRouter()

get_db = database.get_db




@router.get("/blog", response_model = List[schemas.ShowBlog], tags = ["blogs"])
def all(db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


# creating new blog and set the status code
@router.post("/blog", status_code = status.HTTP_201_CREATED, response_model=schemas.ShowBlog, tags = ["blogs"]) 
def create(request : schemas.Blog,db : Session = Depends(get_db)): #created an instance for db
    new_blog = models.Blog(title=request.title,body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

#deleting a particular blog where id == particular id
@router.delete("/blog/{id}", status_code= status.HTTP_204_NO_CONTENT, tags = ["blogs"])
def destroy(id,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return 

#update a particular blog passing the request body schema of blog
@router.put("/blog/{id}",status_code = status.HTTP_202_ACCEPTED, tags = ["blogs"])
def update(id,request:schemas.Blog,db:Session = Depends(get_db)):
    blog =db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    blog.update(request.dict())
    db.commit()
    return  "updated successfully"
           


#show the particular blog with particular id
@router.get("/blog/{id}",status_code = status.HTTP_200_OK, response_model=schemas.ShowBlog, tags = ["blogs"])
def temp(id,db : Session = Depends(get_db)):
    #this is a filter (or say where) in sql and we are getting the fist blog not all the blogs
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail":f"Blog with the id {id} is not available"}
    return blog
