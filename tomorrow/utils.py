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

def camel_to_snake(name):
    return ''.join(['_' + i.lower() if i.isupper() else i for i in name]).lstrip('_')