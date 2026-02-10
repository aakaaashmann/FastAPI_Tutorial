from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def index():
    return {"data": {"name":"Aakash"}}

@app.get("/about")
def about():
    return {"data":{"about page":"Hello this is an about page"}}
