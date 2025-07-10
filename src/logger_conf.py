import logging

def get_logger() -> logging.Logger:
    '''
        We instantiate a logger to handle exceptions better,
    '''
    logger = logging.getLogger('__main__')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger

logger = get_logger()
