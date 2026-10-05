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

# create tables
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

class WaypointCreate(SQLModel):
    latitude: float
    longitude: float
    altitude: int
    sequence: int

# ---------- POST ROUTES ----------
@app.post('/aircraft/{aircraft_id}/routes', response_model=Route)
def create_route(aircraft_id: int):
    with Session(engine) as session:
        aircraft = session.get(Aircraft, aircraft_id) # check if aircraft_id exists
        
        if not aircraft:
            raise HTTPException(status_code=404, detail='Could not find aircraft ID')
        
        route = Route(
            aircraft_id = aircraft_id # associate a route with an aircraft
        ) 

        try:    
            session.add(route)
            session.commit()
            session.refresh(route)
        except Exception:
            session.rollback()
            raise HTTPException(status_code=500, detail='Could not save data')
        
    return route
    

@app.post('/routes/{route_id}/waypoints', response_model=Waypoint)
def waypoints_by_routeid(route_id: int, data: WaypointCreate):
    with Session(engine) as session:
        waypoint = Waypoint(
            latitude = data.latitude,
            longitude = data.longitude,
            altitude = data.altitude,
            sequence = data.sequence,
            route_id = route_id
        )
    
        try:
            session.add(waypoint)
            session.commit()
            session.refresh(waypoint)
        except Exception:
            raise HTTPException(status_code=500, detail='Could not save data')
    
    return waypoint

# ---------- GET ROUTES ----------
@app.get('/aircraft', response_model=list[Aircraft])
def get_aircraft():
    with Session(engine) as session:
        aircrafts = session.exec(select(Aircraft)).all()        
    
    return aircrafts


        