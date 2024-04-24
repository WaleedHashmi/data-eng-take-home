import traceback
import requests
from datetime import datetime
from tomorrow.models import WeatherData
from tomorrow.utils import configure_logging
from tomorrow.config import get_api_key, get_database_url
from tomorrow.db_utils import get_session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

# Configure logger
logger = configure_logging()


def fetch_data():
    try:
        logger.info("Fetching data...")

        db_url = get_database_url()
        session = get_session(db_url)

        locations = [
            "25.8600,-97.4200", "25.9000,-97.5200", "25.9000,-97.4800",
            "25.9000,-97.4400", "25.9000,-97.4000", "25.9200,-97.3800",
            "25.9400,-97.5400", "25.9400,-97.5200", "25.9400,-97.4800",
            "25.9400,-97.4400"
        ]
        url = 'https://api.tomorrow.io/v4/weather/forecast'
        fields = ['temperature', 'windSpeed', 'humidity', 'pressureSurfaceLevel', 'weatherCode', 'windDirection']

        for location in locations:
            params = {
                'location': location,
                'fields': fields,
                'units': 'metric',
                'apikey': get_api_key()
            }

            logger.debug(f"Requesting data for location: {location}")
            logger.debug(f"Payload: {params}")

            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            for item in data['timelines']['minutely']:
                values = item['values']
                record = WeatherData(
                    time=datetime.fromisoformat(item['time']),
                    location=location,
                    cloud_base=values.get('cloudBase'),
                    cloud_ceiling=values.get('cloudCeiling'),
                    cloud_cover=values.get('cloudCover'),
                    dew_point=values.get('dewPoint'),
                    freezing_rain_intensity=values.get('freezingRainIntensity'),
                    humidity=values.get('humidity'),
                    precipitation_probability=values.get('precipitationProbability'),
                    pressure_surface_level=values.get('pressureSurfaceLevel'),
                    rain_intensity=values.get('rainIntensity'),
                    sleet_intensity=values.get('sleetIntensity'),
                    snow_intensity=values.get('snowIntensity'),
                    temperature=values.get('temperature'),
                    temperature_apparent=values.get('temperatureApparent'),
                    uv_health_concern=values.get('uvHealthConcern'),
                    uv_index=values.get('uvIndex'),
                    visibility=values.get('visibility'),
                    weather_code=values.get('weatherCode'),
                    wind_direction=values.get('windDirection'),
                    wind_gust=values.get('windGust'),
                    wind_speed=values.get('windSpeed')
                )

                try:
                    existing_record = session.query(WeatherData
                                                    ).filter_by(time=record.time,location=record.location).one()

                    # Update existing record if exists
                    for attr in vars(record):
                        if attr.startswith('_'):
                            continue
                        setattr(existing_record, attr, getattr(record, attr))

                    existing_record.updated_at = datetime.now()

                except NoResultFound:
                    # If the record doesn't exist, add a new one
                    session.add(record)

            session.commit()

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except IntegrityError as e:
        logger.error(f"Integrity error occurred: {e}")
        session.rollback()  # Rollback the transaction to prevent partial data insertion
    except Exception as err:
        logger.error(f"An error occurred: {err}")
        logger.error(traceback.format_exc())


if __name__ == "__main__":
    fetch_data()
