from fastapi import FastAPI, HTTPException, WebSocketException
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, create_engine, Session, select
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
load_dotenv()

DATABASE_URL = f'postgresql://postgres:{os.getenv('DB_PASSWORD')}@localhost:5432/postgres'


engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event('startup')
def on_startup():
    create_db_and_tables()

class Aircraft(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    latitude: float
    longitude: float
    altitude: int
    grd_speed: int

class Route(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # aircraft foreign key
    aircraft_id: int = Field(foreign_key='aircraft.id')

class Waypoint(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    latitude: float
    longitude: float
    altitude: int
    sequence: int
    # route foreign key
    route_id: int = Field(foreign_key='route.id')
    
@app.post('/')
def post():
    return

@app.get('/')
def get_info():
    return