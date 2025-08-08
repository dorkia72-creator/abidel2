"""
Configuration settings for Persian Sports News Bot
"""
import os
import logging

logger = logging.getLogger(__name__)

class Config:
    def __init__(self):
        # Telegram Bot Token
        self.TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.TELEGRAM_BOT_TOKEN:
            logger.error("TELEGRAM_BOT_TOKEN environment variable is required")
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        
        # OpenAI API Key
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if not self.OPENAI_API_KEY:
            logger.error("OPENAI_API_KEY environment variable is required")
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Bot settings
        self.BOT_USERNAME = os.getenv("BOT_USERNAME", "persian_sports_bot")
        self.MAX_NEWS_PER_REQUEST = int(os.getenv("MAX_NEWS_PER_REQUEST", "5"))
        self.CACHE_TIMEOUT = int(os.getenv("CACHE_TIMEOUT", "300"))  # 5 minutes
        
        # RSS Feed refresh interval (seconds)
        self.FEED_REFRESH_INTERVAL = int(os.getenv("FEED_REFRESH_INTERVAL", "600"))  # 10 minutes
        
        # Request timeout settings
        self.REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
        
        # Logging level
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
        
        # Development mode
        self.DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
        
        logger.info(f"Configuration loaded successfully")
        logger.info(f"Bot username: {self.BOT_USERNAME}")
        logger.info(f"Max news per request: {self.MAX_NEWS_PER_REQUEST}")
        logger.info(f"Debug mode: {self.DEBUG_MODE}")

    def validate_config(self):
        """Validate all required configuration"""
        required_vars = [
            "TELEGRAM_BOT_TOKEN",
            "OPENAI_API_KEY"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(self, var):
                missing_vars.append(var)
        
        if missing_vars:
            error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info("All required configuration variables are present")
        return True
