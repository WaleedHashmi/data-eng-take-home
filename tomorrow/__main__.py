from tomorrow.utils import configure_logging
from tomorrow.scheduler import start_scheduler

logger = configure_logging()

def main():
    
    try:
        logger.info("WELCOME! Starting the scheduler...")
        scheduler = start_scheduler()  
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("User initiated shutdown...")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        if scheduler:
            logger.info("Shutting down the scheduler...")
            scheduler.shutdown()

if __name__ == "__main__":
    main()
