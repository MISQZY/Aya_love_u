import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "venv", ".env")

load_dotenv(dotenv_path)

BOT_TOKEN=os.getenv("BOT_TOKEN")
DB_PATH=os.getenv("DB_PATH")
ADMIN_ID=os.getenv("ADMIN_ID")