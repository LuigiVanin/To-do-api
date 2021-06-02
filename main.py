import uvicorn
from fastapi import FastAPI
from config import *
from routers import *
from models import *

Base.metadata.create_all(engine)
app = FastAPI()

app.include_router(logon_router)
app.include_router(login_router)
app.include_router(user_router)


@app.get(path="/")
def root_test():
    return {"detail": "Hello ToDo project"}


if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
