from pathlib import Path
import logging
import os

SECRETS_JSON = "secrets.json" #os.getenv("SECRETS_JSON")
if SECRETS_JSON is None:
    logging.debug("Cannot find location of secrets.json from environment variable (bot not started with init.sh), falling back to base directory.")
    SECRETS_JSON = "secrets.json"
    os.environ["SECRETS_JSON"] = SECRETS_JSON

DB_NAME = "data/tables.db"
