from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from tomorrow.config import get_database_url
from tomorrow.models import WeatherData
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
        locations = db.query(WeatherData.location).distinct().all()
        return [location[0] for location in locations]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/latest_weather/{location}", response_model=WeatherDataResponse)
async def get_latest_weather(location: str) -> WeatherDataResponse:
    try:
        db = SessionLocal()
        latest_weather = db.query(WeatherData).filter(WeatherData.location == location).order_by(desc(WeatherData.time)).first()
        if not latest_weather:
            raise HTTPException(status_code=404, detail="Weather data not found for this location")
        
        # Create a WeatherDataResponse object from the latest_weather
        weather_response = WeatherDataResponse(
            location=latest_weather.location,
            temperature=latest_weather.temperature,
            humidity=latest_weather.humidity,
            wind_speed=latest_weather.wind_speed,
            cloud_ceiling=latest_weather.cloud_ceiling,
            cloud_base=latest_weather.cloud_base,
            cloud_cover=latest_weather.cloud_cover,
            dew_point=latest_weather.dew_point,
            freezing_rain_intensity=latest_weather.freezing_rain_intensity,
            precipitation_probability=latest_weather.precipitation_probability,
            pressure_surface_level=latest_weather.pressure_surface_level,
            rain_intensity=latest_weather.rain_intensity,
            sleet_intensity=latest_weather.sleet_intensity,
            snow_intensity=latest_weather.snow_intensity,
            temperature_apparent=latest_weather.temperature_apparent,
            uv_health_concern=latest_weather.uv_health_concern,
            uv_index=latest_weather.uv_index,
            visibility=latest_weather.visibility,
            weather_code=latest_weather.weather_code,
            wind_direction=latest_weather.wind_direction,
            wind_gust=latest_weather.wind_gust,
            time=latest_weather.time
        )
        return weather_response
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@app.get("/last_n_rows/{location}", response_model=List[WeatherDataResponse])
async def get_last_n_rows(location: str, n: Optional[int] = 10) -> List[WeatherDataResponse]:
    try:
        db = SessionLocal()
        last_n_rows = db.query(WeatherData).filter(WeatherData.location == location).order_by(desc(WeatherData.time)).limit(n).all()
        if not last_n_rows:
            raise HTTPException(status_code=404, detail="Weather data not found for this location")
        return last_n_rows
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
