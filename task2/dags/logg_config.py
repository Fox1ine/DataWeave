import logging
import os
from dotenv import load_dotenv

dotenv_path = os.getenv("DOTENV_PATH")
load_dotenv(dotenv_path)
LOG_DIR = os.getenv("LOGGING_PATH", "task2/logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "task2.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("task2")
