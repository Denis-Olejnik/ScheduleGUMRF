from loguru import logger

logger.add("logger.log", format="{time} {level} {message}", level="DEBUG")
