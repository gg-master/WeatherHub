from pathlib import Path
from dotenv import load_dotenv
from app import create_app

ENV_PATH = "./dev.env"

if __name__ == "__main__":
    load_dotenv(Path(ENV_PATH))
    app = create_app()
    app.run(host="0.0.0.0", debug=True)