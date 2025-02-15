## will create the entire template for the project
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]:%(message)s:')

list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "setup.py",
    "app.py",
    "research/trial.ipynb",
]

for filpath in list_of_files:
    filpath = Path(filpath)
    filedir , filename = os.path.split(filpath)

    if filedir!= "":     # create the folder
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir} for the file: {filename}")

    if (not os.path.exists(filpath) or os.path.getsize(filpath) == 0):   # create the file
        with open(filpath, "w") as f:
            pass
            logging.info(f"Created empty file: {filpath}")
    else:

        logging.info(f"file: {filename} is already present in the directory")




        