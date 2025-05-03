import os
import json

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from sqlmodel import SQLModel, create_engine, Session, select

from .models import *

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
SQLModel.metadata.create_all(engine)

app = FastAPI(default_response_class=HTMLResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="../static"), name="static")

@app.get("/")
async def root():
    with open("../templates/index.html", "r") as fp:
        return fp.read()


@app.post("/add-constellation")
async def add_constellation(
        scientific_name: str = Form(...),
        informal_name: str = Form(...),
        star_coords: str = Form(...)
    ):
    star_coords = json.dumps([s.strip() for s in star_coords.split(",")])
    constellation = Constellation(scientific_name=scientific_name, informal_name=informal_name, star_coords=star_coords)
    scientific_checker = select(Constellation).where(Constellation.scientific_name == scientific_name)
    informal_checker = select(Constellation).where(Constellation.informal_name == informal_name)
    with Session(engine) as session:
        if session.exec(scientific_checker).all():
            return "That scientific name is already in the database. Try another!"
        if session.exec(informal_checker).all():
            return "That informal name is already in the database. Try another!"
        session.add(constellation)
        session.commit()
        session.refresh(constellation)
    return f"{scientific_name} has been added to our database!"

