"""
Telegram Bot implementation for Esteghlal News Aggregator
"""
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
from rss_parser import RSSParser
from config import Config
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class EsteghlalNewsBot:
    def __init__(self):
        self.config = Config()
        self.rss_parser = RSSParser()
        if not self.config.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        self.app = Application.builder().token(self.config.TELEGRAM_BOT_TOKEN).build()
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup command and callback handlers"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CallbackQueryHandler(self.latest_news_handler, pattern="^latest_news$"))
        self.app.add_handler(CallbackQueryHandler(self.full_news_handler, pattern="^full_news_\\d+$"))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        try:
            keyboard = [
                [InlineKeyboardButton("📰 اخبار روز استقلال", callback_data="latest_news")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "به ربات آبی دل خوش آمدید! 💙\nیکی از گزینه‌های زیر را انتخاب کنید:", 
                reply_markup=reply_markup
            )
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            await update.message.reply_text("خطا در اجرای دستور. لطفاً دوباره تلاش کنید.")

    def fetch_full_article(self, url):
        """Fetch full article content using web scraping"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract paragraphs
            paragraphs = soup.find_all("p")
            text = "\n\n".join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 30])
            
            # Limit to 3000 characters to avoid long messages
            return text[:3000] if text else "متأسفانه متن کامل خبر قابل دریافت نیست."
            
        except Exception as e:
            logger.error(f"Error fetching full article from {url}: {e}")
            return "متأسفانه متن کامل خبر قابل دریافت نیست."

    async def latest_news_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle latest news callback"""
        query = update.callback_query
        await query.answer()
        
        try:
            news_list = await self.rss_parser.get_esteghlal_news()
            
            if not news_list:
                await query.message.reply_text("در حال حاضر خبری در دسترس نیست.")
                return

            # Send each news item with a button to view full text
            for idx, news in enumerate(news_list, start=1):
                buttons = [[InlineKeyboardButton("📖 نمایش متن کامل", callback_data=f"full_news_{idx}")]]
                reply_markup = InlineKeyboardMarkup(buttons)
                
                summary = news.get('description', '')[:300] + '...' if len(news.get('description', '')) > 300 else news.get('description', '')
                text = f"✅ {news['title']}\n\n{summary}\n\n{news['link']}"
                
                # Store the link in user_data for retrieval
                context.user_data[f"full_news_{idx}"] = news["link"]
                
                await query.message.reply_text(text, reply_markup=reply_markup)
                
        except Exception as e:
            logger.error(f"Error in latest news handler: {e}")
            await query.message.reply_text("خطا در دریافت اخبار. لطفاً دوباره تلاش کنید.")

    async def full_news_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle full news callback"""
        query = update.callback_query
        await query.answer()
        
        try:
            key = query.data
            url = context.user_data.get(key)
            
            if not url:
                await query.message.reply_text("لینک خبر پیدا نشد.")
                return
            
            # Fetch full article content
            full_text = self.fetch_full_article(url)
            await query.message.reply_text(full_text)
            
        except Exception as e:
            logger.error(f"Error in full news handler: {e}")
            await query.message.reply_text("خطا در دریافت متن کامل. لطفاً دوباره تلاش کنید.")











    async def run(self):
        """Start the bot"""
        logger.info("Esteghlal News Bot is starting...")
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()
        
        logger.info("Bot is running. Press Ctrl+C to stop.")
        
        try:
            import asyncio
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        finally:
            await self.app.stop()
