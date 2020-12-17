import logging
import os

log_level_code = getattr(logging, os.environ.get('LOG_LEVEL', ''), logging.DEBUG)
logging.basicConfig(
    format='%(asctime)s %(levelname)s [%(name)s]: %(message)s'
    , datefmt='%Y-%m-%d %I:%M:%S %p'
    , level=log_level_code)

# Quiet chatty libs
logging.getLogger('azure.core.pipeline.policies').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)
# logging.getLogger('msrest').setLevel(logging.ERROR)
# logging.getLogger('zeep').setLevel(logging.ERROR)