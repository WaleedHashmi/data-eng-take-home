from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class WeatherDataResponse(BaseModel):
    time: datetime
    location: str
    temperature: float
    wind_speed: float
    cloud_base: Optional[float]
    cloud_ceiling: Optional[float]
    cloud_cover: Optional[float]
    humidity: Optional[float]
    dew_point: Optional[float]
    freezing_rain_intensity: Optional[float]
    precipitation_probability: Optional[float]
    pressure_surface_level: Optional[float]
    rain_intensity: Optional[float]
    sleet_intensity: Optional[float]
    snow_intensity: Optional[float]
    temperature_apparent: Optional[float]
    uv_health_concern: Optional[int]
    uv_index: Optional[int]
    visibility: Optional[float]
    weather_code: Optional[int]
    wind_direction: Optional[float]
    wind_gust: Optional[float]
