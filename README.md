# Todo Project

## Installation

- Make sure you're on the venv (python 3.10)
- Install requirements: `pip install -r requirements.txt`
- Create `.env.local` and `.env.docker` files based on the `.env.example` file
- Run the database: `docker-compose up -d db`

## Running the project

### Run locally

Run the following command:

```bash
python main.py --help
```

### Run via docker compose

Run the following command:

```bash
docker-compose run --rm cli --help 
```