import logging
import logging.handlers
import sys

def setup_logging():
    # Create logger
    logger = logging.getLogger('agent')
    logger.setLevel(logging.INFO)
    
    # Create formatter with emojis and better spacing
    formatter = logging.Formatter(
        '\n🤖 [%(name)s] [%(filename)s] [%(funcName)s] [%(levelname)s]\n'
        '⏰ %(asctime)s 💬 Message: %(message)s\n'
        '-------------------------------------------\n'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler
    file_handler = logging.handlers.RotatingFileHandler(
        'agent.log',
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

# Initialize logging
logger = setup_logging()