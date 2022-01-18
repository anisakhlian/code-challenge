import logging
import os
from .pg_helpers.sqlalchemy_helper import SqlalchemyHelper
from .pg_documents import PgDocument

# Initialize Logging
logging.basicConfig()
loggers = ["pynamodb", "elasticsearch.trace"]
for logger in loggers:
    log = logging.getLogger(logger)
    log.setLevel(logging.INFO)
    if os.environ.get("DEBUG"):
        log.setLevel(logging.DEBUG)
    log.propagate = True
loggers = ["elasticsearch"]
for logger in loggers:
    log = logging.getLogger(logger)
    log.setLevel(logging.WARNING)
    if os.environ.get("DEBUG"):
        log.setLevel(logging.DEBUG)
    log.propagate = True

db_session = SqlalchemyHelper.session
