from fastapi import FastAPI, HTTPException, WebSocketException
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlalchemy.engine import URL
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from models import Aircraft, Route, Waypoint, WaypointCreate, SimulationRun

app = FastAPI()
load_dotenv()

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password=os.environ["DB_PASSWORD"],
    host="127.0.0.1",
    port=5433,
    database="postgres"
)

engine = create_engine(DATABASE_URL, echo=True)

# create tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event('startup')
def on_startup():
    create_db_and_tables()

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
        route_id_check = session.get(Route, route_id)
        
        if not route_id_check:
            raise HTTPException(status_code=404, detail='Could not find route ID')
        
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
            session.rollback()
            raise HTTPException(status_code=500, detail='Could not save data')
    
    return waypoint

@app.post('/routes/{route_id}/simulations', response_model=SimulationRun)
def create_simulation(route_id: int):
    with Session(engine) as session:
        route_id_check = session.get(Route, route_id)
        
        if not route_id_check:
            raise HTTPException(status_code=404, detail='Couldnt find route id')
        
        simulation = SimulationRun(
            
        )

# ---------- GET ROUTES ----------
@app.get('/aircraft', response_model=list[Aircraft])
def get_aircraft():
    with Session(engine) as session:
        aircrafts = session.exec(select(Aircraft)).all()        
    
    return aircrafts

@app.get('/routes/{route_id}/waypoints', response_model=list[Waypoint])
def get_routes(route_id: int):
    with Session(engine) as session:
        route_id_check = session.get(Route, route_id)
        if not route_id_check:
            raise HTTPException(status_code=404, detail='Couldnt find route id')
        
        statement = select(Waypoint).where(
            Waypoint.route_id == route_id
        ).order_by(Waypoint.sequence)
        
        results = session.exec(statement).all()

        return results
    


        