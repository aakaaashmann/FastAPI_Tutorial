from typing import List
from pydantic import BaseModel

#blog schema
class Blog(BaseModel):
    title : str
    body : str

class BlogBase(Blog):
    class Config():
        orm_mode = True


#for user schema
class User(BaseModel):
    name : str
    email : str
    password : str

class ShowUser(BaseModel):
    name : str
    email : str
    blogs : List[Blog] =[]
    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    title : str
    body : str
    creator : ShowUser
    class Config():
        orm_mode = True