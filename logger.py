import logging
import logging.handlers


def init_logger(name, level, f=None):
    level = getattr(logging, level.upper(), None)
    logger = logging.getLogger(name)
    logger.propagate = False  # don't propagate to root logger!
    logger.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(process)d - %(thread)d - %(name)s - %(levelname)s - %(message)s')

    if f:
        fh = logging.handlers.RotatingFileHandler(f, maxBytes=1024 * 1024 * 50, backupCount=5)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    else:
        sh = logging.StreamHandler()
        sh.setLevel(level)
        sh.setFormatter(formatter)
        logger.addHandler(sh)
