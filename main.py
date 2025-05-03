from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from sqlmodel import SQLModel, create_engine, Session


engine = create_engine("sqlite://", echo=True)
SQLModel.metadata.create_all(engine)

app = FastAPI(default_response_class=HTMLResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    with open("index.html", "r") as fp:
        return fp.read()

