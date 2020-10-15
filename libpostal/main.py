import logging

logging.basicConfig(format='%(asctime)s %(levelname)s [%(name)s]: %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":

    logger.info('hello world')
