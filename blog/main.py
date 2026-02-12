from fastapi import FastAPI , Depends
from . import schemas , models
from .database import engine , SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# creating new blog
@app.post("/blog")
def create(request : schemas.Blog,db : Session = Depends(get_db)): #created an instance for db
    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

#to fetch all the blogs
@app.get("/blog")
def all(db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

#show the particular blog with particular id
@app.get("/blog/{id}")
def temp(id,db : Session = Depends(get_db)):
    #this is a filter (or say where) in sql and we are getting the fist blog not all the blogs
    blog = db.query(models.Blog).filter(models.Blog.id == id).first() 
    return blog

