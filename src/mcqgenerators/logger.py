import logging
import os
from datetime import datetime


# Create a unique log file name using the current date and time
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"


# Create logs directory in the project root
log_path = os.path.join(os.getcwd(), "logs")

os.makedirs(log_path, exist_ok=True)


# Complete path of the log file
LOG_FILEPATH = os.path.join(log_path, LOG_FILE)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILEPATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)
