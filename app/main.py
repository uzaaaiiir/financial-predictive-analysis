from fastapi import FastAPI
from .routes import router


app = FastAPI()

app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the QInvst Automation Tool!"}
