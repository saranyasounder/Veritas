import logging

def get_logger(name: str):
    # get or create a logger with the given name
    # if a logger with this name already exists, return that one
    # this prevents duplicate loggers being created
    logger = logging.getLogger(name)
    
    # set the minimum severity level to capture
    # DEBUG means capture everything — debug, info, warning, error, critical
    logger.setLevel(logging.DEBUG)
    
    # stream handler — writes log output to the terminal
    ch = logging.StreamHandler()
    
    # file handler — writes log output to veritas.log
    # creates the file if it doesn't exist
    fh = logging.FileHandler("veritas.log")
    
    # set minimum level for terminal output
    ch.setLevel(logging.DEBUG)
    
    # set minimum level for file output
    fh.setLevel(logging.DEBUG)
    
    # define the format of each log entry
    # %(asctime)s   — timestamp e.g. 2026-05-31 10:23:45
    # %(name)s      — name passed in e.g. evaluator.pipeline
    # %(levelname)s — severity e.g. INFO, ERROR, WARNING
    # %(message)s   — the actual log message
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # attach the formatter to both handlers
    # so both terminal and file output look the same
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    
    # attach both handlers to the logger
    # now every log call writes to both terminal and file
    logger.addHandler(ch)
    logger.addHandler(fh)
    
    # return the fully configured logger
    # caller does: logger = get_logger(__name__)
    return logger