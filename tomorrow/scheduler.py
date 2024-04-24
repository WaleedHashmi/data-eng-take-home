from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from tomorrow.data_fetcher import fetch_data
from tomorrow.utils import configure_logging

logger = configure_logging()

def start_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(fetch_data, 'interval', hours=1, next_run_time=datetime.now())
    return scheduler
