from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_data'
    time = Column(DateTime, primary_key=True)
    location = Column(String, primary_key=True)
    cloud_base = Column(Float)
    cloud_ceiling = Column(Float)
    cloud_cover = Column(Float)
    dew_point = Column(Float)
    freezing_rain_intensity = Column(Float)
    humidity = Column(Float)
    precipitation_probability = Column(Float)
    pressure_surface_level = Column(Float)
    rain_intensity = Column(Float)
    sleet_intensity = Column(Float)
    snow_intensity = Column(Float)
    temperature = Column(Float)
    temperature_apparent = Column(Float)
    uv_health_concern = Column(Integer)
    uv_index = Column(Integer)
    visibility = Column(Float)
    weather_code = Column(Integer)
    wind_direction = Column(Float)
    wind_gust = Column(Float)
    wind_speed = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
