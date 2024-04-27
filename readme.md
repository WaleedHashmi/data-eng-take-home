# Amperon Data Engineering Take Home Assignment

This repository provides a solution to scrape weather forecasts and historical data using the Tomorrow IO API, targeting specific geographic locations, and store this data in a PostgreSQL database. It also includes facilities for querying this data using SQL and visualizing it through various services.

## System Overview

The system is composed of multiple services:

- **PostgreSQL Database**:
  - **Port**: 5432
  - Stores data from the Tomorrow IO API.

- **Scraper Service**:
  - Runs hourly, scraping data for predefined locations and storing it in the database.

- **Jupyter Notebook**:
  - **URL**: [localhost:8888](http://localhost:8888)
  - Facilitates data visualization.

- **FastAPI Server**:
  - **URL**: [localhost:8000/docs](http://localhost:8000/docs)
  - Provides API access to the data.

- **React Frontend**:
  - **URL**: [localhost:3000](http://localhost:3000)
  - Offers a graphical interface for data interaction.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:
   ```shell
   git clone [repository-url]
   ```

2. Navigate to the project directory:
   ```shell
   cd [project-directory]
   ```

3. Build and start the containers:
   ```shell
   docker compose up --build
   ```

### Usage

- **Access the PostgreSQL database**:
  - **Host**: localhost
  - **Port**: 5432
  - **Database**: tomorrow
  - **Username**: postgres
  - **Password**: postgres

- **Initialize the database**:
  - Scripts located at `./scripts/init-db.sql` run automatically on container start.

- **Jupyter Notebook**:
  - Open [localhost:8888](http://localhost:8888) in your browser.

- **FastAPI Server** (Optional):
  - Documentation and API access available at [localhost:8000/docs](http://localhost:8000/docs).

- **React Frontend** (Optional):
  - Interface accessible at [localhost:3000](http://localhost:3000).

## Repository Structure

- `scripts/`: Contains SQL scripts for database initialization.
- `scraper.py`: Implements the scraping logic.
- `notebook.ipynb`: Notebook for results visualization.
- `api.py`: FastAPI server application (Optional).
- `frontend/`: React application files (Optional).

## Technologies

- **Python**: Primary programming language.
- **Docker**: For containerization.
- **PostgreSQL**: Database management.
- **Jupyter Notebook**: For visualization.
- **FastAPI & React**: For API and frontend development - These were deployed as additional services

## Answering the Questions: 
- Latest Weather is available both on the jupyer notebook. and on reactJS front end which fetches it thought the fastAPI endpoint which uses SQL. This is to show that this system can simultaneously run a real-time webapp and run notebook analyses at the same time
- Other Timeseries and map visualisations are in the notebook

## Best Engineering Practices:
- Follow a modular and organized directory structure to improve code maintainability.
- Implement automated unit testing using pytest and a stand alone integration testing 
- Use a Russ linter and adhere to coding style guidelines to ensure consistent code formatting.
- Implement error handling and logging to improve system reliability and troubleshoot issues.
- Optimize code performance and efficiency to enhance system scalability.


## Followups

For any questions and/or followups feel free to reach out at waleedahmedhashmi@gmail.com