from dotenv import load_dotenv
load_dotenv(
    dotenv_path=".env.local"
)

from app.cli import app

if __name__ == '__main__':
    app()
