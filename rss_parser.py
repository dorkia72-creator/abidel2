"""
RSS Feed Parser for Persian Sports News Sources
"""
import feedparser
import logging
from datetime import datetime
from typing import List, Dict, Optional
import asyncio
import aiohttp
from config import Config

logger = logging.getLogger(__name__)

class RSSParser:
    def __init__(self):
        self.config = Config()
        self.rss_feeds = {
            'varzesh3': 'https://www.varzesh3.com/rss/all',
            'tarafdari': 'https://www.tarafdari.com/rss/all',
            'footballi': 'https://footballi.net/rss/news',
            'metafootball': 'https://metafootball.com/fa/news/feed',
            'khabarvarzeshi': 'https://www.khabarvarzeshi.com/rss'
        }
        
        # Category keywords for Persian sports
        self.category_keywords = {
            'football': ['فوتبال', 'پرسپولیس', 'استقلال', 'تیم ملی', 'لیگ برتر', 'جام جهانی'],
            'basketball': ['بسکتبال', 'سوپرلیگ بسکتبال'],
            'wrestling': ['کشتی', 'رزمی', 'جودو', 'کاراته', 'تکواندو'],
            'volleyball': ['والیبال', 'سایپا', 'کالای خودرو'],
            'athletics': ['دو و میدانی', 'دومیدانی', 'دوومیدانی', 'المپیک']
        }

    async def get_latest_news(self, limit: int = 10) -> List[Dict]:
        """Get latest news from all RSS feeds"""
        try:
            all_news = []
            
            async with aiohttp.ClientSession() as session:
                tasks = []
                for source_name, feed_url in self.rss_feeds.items():
                    task = self._fetch_feed(session, source_name, feed_url)
                    tasks.append(task)
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for result in results:
                    if isinstance(result, Exception):
                        logger.error(f"Error fetching feed: {result}")
                        continue
                    if result and isinstance(result, list):
                        all_news.extend(result)
            
            # Sort by publication date (newest first)
            all_news.sort(key=lambda x: x.get('published_parsed', datetime.min), reverse=True)
            
            return all_news[:limit]
            
        except Exception as e:
            logger.error(f"Error getting latest news: {e}")
            return []

    async def get_news_by_category(self, category: str, limit: int = 10) -> List[Dict]:
        """Get news filtered by category"""
        try:
            all_news = await self.get_latest_news(limit * 3)  # Get more to filter
            
            if category not in self.category_keywords:
                return all_news[:limit]
            
            keywords = self.category_keywords[category]
            filtered_news = []
            
            for news_item in all_news:
                title = news_item.get('title', '').lower()
                description = news_item.get('description', '').lower()
                
                # Check if any keyword exists in title or description
                if any(keyword in title or keyword in description for keyword in keywords):
                    filtered_news.append(news_item)
                    
                if len(filtered_news) >= limit:
                    break
            
            return filtered_news
            
        except Exception as e:
            logger.error(f"Error getting news by category {category}: {e}")
            return []

    async def get_esteghlal_news(self, limit: int = 5) -> List[Dict]:
        """Get Esteghlal-specific news from all RSS feeds"""
        try:
            all_news = []
            
            async with aiohttp.ClientSession() as session:
                tasks = []
                for source_name, feed_url in self.rss_feeds.items():
                    task = self._fetch_feed(session, source_name, feed_url)
                    tasks.append(task)
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for result in results:
                    if isinstance(result, Exception):
                        logger.error(f"Error fetching feed: {result}")
                        continue
                    if result and isinstance(result, list):
                        all_news.extend(result)
            
            # Filter for Esteghlal news
            esteghlal_news = []
            for news_item in all_news:
                title = news_item.get('title', '').lower()
                description = news_item.get('description', '').lower()
                
                # Check if "استقلال" is in title or description
                if 'استقلال' in title or 'استقلال' in description:
                    esteghlal_news.append(news_item)
                    
                if len(esteghlal_news) >= limit:
                    break
            
            # Sort by publication date (newest first)
            esteghlal_news.sort(key=lambda x: x.get('published_parsed', datetime.min), reverse=True)
            
            return esteghlal_news[:limit]
            
        except Exception as e:
            logger.error(f"Error getting Esteghlal news: {e}")
            return []

    async def get_all_news(self, limit: int = 20) -> List[Dict]:
        """Get all news from all sources"""
        return await self.get_latest_news(limit)

    async def _fetch_feed(self, session: aiohttp.ClientSession, source_name: str, feed_url: str) -> List[Dict]:
        """Fetch and parse a single RSS feed"""
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with session.get(feed_url, timeout=timeout) as response:
                if response.status != 200:
                    logger.warning(f"Failed to fetch {source_name}: HTTP {response.status}")
                    return []
                
                content = await response.text()
                
            # Parse RSS feed
            feed = feedparser.parse(content)
            
            if feed.bozo:
                logger.warning(f"Feed {source_name} has parsing issues: {feed.bozo_exception}")
            
            news_items = []
            
            for entry in feed.entries[:10]:  # Limit per source
                try:
                    news_item = {
                        'title': self._clean_text(entry.get('title', 'بدون عنوان')),
                        'description': self._clean_text(entry.get('summary', entry.get('description', ''))),
                        'link': entry.get('link', ''),
                        'published': self._format_date(entry.get('published', '')),
                        'published_parsed': entry.get('published_parsed', datetime.min.timetuple()),
                        'source': source_name
                    }
                    
                    # Skip if essential fields are missing
                    if not news_item['title'] or not news_item['link']:
                        continue
                        
                    news_items.append(news_item)
                    
                except Exception as e:
                    logger.error(f"Error parsing entry from {source_name}: {e}")
                    continue
            
            logger.info(f"Successfully fetched {len(news_items)} items from {source_name}")
            return news_items
            
        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching feed from {source_name}")
            return []
        except Exception as e:
            logger.error(f"Error fetching feed from {source_name}: {e}")
            return []

    def _clean_text(self, text: str) -> str:
        """Clean and normalize Persian text"""
        if not text:
            return ""
        
        # Remove HTML tags
        import re
        text = re.sub('<[^<]+?>', '', text)
        
        # Normalize Persian text
        text = text.replace('ي', 'ی').replace('ك', 'ک')
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()

    def _format_date(self, date_str: str) -> str:
        """Format publication date to Persian"""
        try:
            if not date_str:
                return "تاریخ نامشخص"
            
            # Parse the date string
            try:
                from email.utils import parsedate_to_datetime
                dt = parsedate_to_datetime(date_str)
                if dt:
                    # Format in Persian
                    persian_months = [
                        'ژانویه', 'فوریه', 'مارس', 'آپریل', 'مه', 'ژوئن',
                        'ژوئیه', 'آگوست', 'سپتامبر', 'اکتبر', 'نوامبر', 'دسامبر'
                    ]
                    
                    persian_date = f"{dt.day} {persian_months[dt.month-1]} {dt.year}"
                    persian_time = f"{dt.hour:02d}:{dt.minute:02d}"
                    
                    return f"{persian_date} - {persian_time}"
            except:
                pass
            
            return date_str
            
        except Exception as e:
            logger.error(f"Error formatting date {date_str}: {e}")
            return "تاریخ نامشخص"
