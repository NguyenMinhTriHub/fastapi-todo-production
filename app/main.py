from fastapi import FastAPI
from app import model
from app.core.database import engine
from app.routers import todo_router, auth_router

model.Base.metadata.create_all(bind=engine)
app = FastAPI(title="To-do App Level 8")

app.include_router(auth_router.router) 
app.include_router(todo_router.router)

@app.get("/")
def read_root():
    return {"message": "Application is Live"}