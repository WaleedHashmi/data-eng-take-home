import os

def get_database_url():
    db_user = os.getenv('PGUSER', 'postgres')
    db_pass = os.getenv('PGPASSWORD', 'postgres')
    db_host = os.getenv('PGHOST', 'postgres')  
    db_port = os.getenv('PGPORT', '5432')
    db_name = os.getenv('PGDATABASE', 'tomorrow')
    return f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

def get_api_key():
    return os.getenv('API_KEY')
