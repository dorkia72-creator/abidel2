#!/usr/bin/env python3
"""
Persian Sports News Aggregator Telegram Bot
Entry point for the application
"""
import asyncio
import logging
from bot import EsteghlalNewsBot

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Main function to start the bot"""
    try:
        logger.info("Starting Esteghlal News Bot...")
        bot = EsteghlalNewsBot()
        await bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
