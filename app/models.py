from typing import Optional, List, Literal
from sqlmodel import SQLModel, Field, create_engine, Session, select, CheckConstraint
from datetime import datetime

class Aircraft(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    jbsim_model: str

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

StatusOptions = Literal["Queued", "Running", "Completed", "Failed"]  
class SimulationRun(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    route_id: int = Field(foreign_key='route.id')
    created_at: datetime
    status: StatusOptions = Field(
        default="Queued",
        __table_args__ = (
            CheckConstraint(
            "status IN ('Queued', 'Running', 'Completed', 'Failed')",
            name="check_simulation_status"
        ),
    ))

