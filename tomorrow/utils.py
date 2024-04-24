import logging
import os

def configure_logging():
    log_directory = "./logs/"  
    log_filename = os.path.join(log_directory, 'application.log')
    
    if not os.path.exists(log_directory):
        os.makedirs(log_directory) 

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()  
        ]
    )
    return logging.getLogger(__name__)