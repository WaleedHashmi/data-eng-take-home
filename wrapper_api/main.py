from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from tomorrow.config import get_database_url
from tomorrow.models import WeatherDataMinutely, WeatherDataDaily, WeatherDataHourly
from wrapper_api.models import WeatherDataResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

SQLALCHEMY_DATABASE_URL = get_database_url()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/locations/", response_model=List[str])
async def get_all_locations() -> List[str]:
    try:
        db = SessionLocal()
        locations = db.query(WeatherDataMinutely.location).distinct().all()
        return [location[0] for location in locations]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/latest_weather/{location}", response_model=dict)
async def get_latest_weather(location: str, granularity: str = Query("minutely", enum=["minutely", "hourly", "daily"])) -> dict:
    model_map = {
        "minutely": WeatherDataMinutely,
        "hourly": WeatherDataHourly,
        "daily": WeatherDataDaily
    }
    model = model_map.get(granularity)
    try:
        db: Session = SessionLocal()
        latest_weather = db.query(model).filter(model.location == location).order_by(desc(model.time)).first()
        if not latest_weather:
            raise HTTPException(status_code=404, detail="Weather data not found for this location")

        return {column.name: getattr(latest_weather, column.name) for column in model.__table__.columns}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/last_n_rows/{location}", response_model=List[dict])
async def get_last_n_rows(location: str, granularity: str = Query("minutely", enum=["minutely", "hourly", "daily"]), n: Optional[int] = 10) -> List[dict]:
    model_map = {
        "minutely": WeatherDataMinutely,
        "hourly": WeatherDataHourly,
        "daily": WeatherDataDaily
    }
    model = model_map.get(granularity)
    try:
        db: Session = SessionLocal()
        last_n_rows = db.query(model).filter(model.location == location).order_by(desc(model.time)).limit(n).all()
        if not last_n_rows:
            raise HTTPException(status_code=404, detail="Weather data not found for this location")
        
        return [{column.name: getattr(row, column.name) for column in model.__table__.columns} for row in last_n_rows]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()