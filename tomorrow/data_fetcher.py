import traceback
import requests
from datetime import datetime
from tomorrow.models import WeatherDataDaily, WeatherDataHourly, WeatherDataMinutely
from tomorrow.utils import configure_logging, camel_to_snake
from tomorrow.config import get_api_key, get_database_url
from tomorrow.db_utils import get_session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

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

            timelines = {
                'daily': WeatherDataDaily,
                'hourly': WeatherDataHourly,
                'minutely': WeatherDataMinutely
            }

            for timeline_key, model_class in timelines.items():
                for item in data['timelines'][timeline_key]:
                    record = model_class(time=datetime.fromisoformat(item['time']), location=location)
                    model_fields = {camel_to_snake(column.name): column.name for column in model_class.__table__.columns}

                    for key, value in item['values'].items():
                        snake_key = camel_to_snake(key)
                        if snake_key in model_fields:
                            setattr(record, snake_key, value)

                    try:
                        existing_record = session.query(model_class).filter_by(time=record.time, location=record.location).one()
                        for key in model_fields:
                            setattr(existing_record, key, getattr(record, key))
                        existing_record.updated_at = datetime.now()
                    except NoResultFound:
                        session.add(record)

            session.commit()

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except IntegrityError as e:
        logger.error(f"Integrity error occurred: {e}")
        session.rollback()
    except Exception as err:
        logger.error(f"An error occurred: {err}")
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    fetch_data()
