import logging
import os
from datetime import datetime


LOG_FILES=f"{datetime.now().strftime('%m_%d_%Y_%M_%S')}.log"
logs_path=os.path.join(os.getcwd(),'logs',LOG_FILES)
os.makedirs(logs_path,exist_ok=True)

LOG_FILES_PATH =os.path.join(logs_path,LOG_FILES)

logging.basicConfig(
filename=LOG_FILES_PATH,
 format="%(asctime)s - %(levelname)s - %(message)s",
 level=logging.INFO,
 force=True,
)

if __name__ == "__main__":
    logging.info('logging has started')