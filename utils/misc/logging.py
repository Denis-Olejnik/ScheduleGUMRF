from loguru import logger

logger.add("app.log", format="{time} {level} {message}", rotation="10 MB", compression="zip",
           level="DEBUG")
