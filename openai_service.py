"""
OpenAI Service for Persian Text Summarization and Analysis
"""
import json
import os
import logging
from typing import Optional
from openai import OpenAI

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"

    async def summarize_persian_news(self, text: str) -> str:
        """Summarize Persian news article"""
        try:
            if not text or len(text.strip()) < 50:
                return "متن کوتاه است و نیازی به خلاصه‌سازی ندارد."
            
            prompt = f"""
لطفاً متن خبری فارسی زیر را به صورت مختصر و مفید خلاصه کنید. خلاصه باید:
- حداکثر 3-4 جمله باشد
- نکات مهم و کلیدی را شامل شود
- به زبان فارسی و با قواعد درست نوشته شود
- خوانا و روان باشد

متن خبر:
{text}
"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "شما یک خلاصه‌نویس حرفه‌ای هستید که متخصص در خلاصه‌سازی اخبار ورزشی فارسی است."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            summary = response.choices[0].message.content
            if summary:
                summary = summary.strip()
            else:
                summary = "خلاصه‌ای تولید نشد."
            
            # Validate summary
            if len(summary) < 20:
                return "خلاصه‌ای از این خبر تهیه نشد."
            
            return summary
            
        except Exception as e:
            logger.error(f"Error summarizing Persian news: {e}")
            return "خطا در تولید خلاصه. متن اصلی نمایش داده می‌شود."

    async def analyze_news_sentiment(self, text: str) -> dict:
        """Analyze sentiment of Persian news text"""
        try:
            prompt = f"""
لطفاً احساس و تون کلی متن خبری فارسی زیر را تحلیل کنید.
پاسخ را به صورت JSON با فرمت زیر ارائه دهید:
{{"sentiment": "positive/negative/neutral", "confidence": 0.85, "reasoning": "دلیل تحلیل"}}

متن:
{text}
"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "شما یک تحلیلگر احساسات متن فارسی هستید."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=150,
                temperature=0.2
            )
            
            content = response.choices[0].message.content
            if content:
                result = json.loads(content)
            else:
                raise Exception("No content received")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {
                "sentiment": "neutral",
                "confidence": 0.0,
                "reasoning": "خطا در تحلیل احساسات"
            }

    async def categorize_sports_news(self, title: str, description: str) -> str:
        """Categorize sports news into Persian categories"""
        try:
            text = f"عنوان: {title}\nتوضیحات: {description}"
            
            prompt = f"""
لطفاً این خبر ورزشی را در یکی از دسته‌بندی‌های زیر قرار دهید:
- فوتبال
- بسکتبال
- والیبال
- کشتی و رزمی
- دو و میدانی
- سایر ورزش‌ها

فقط نام دسته را بنویسید.

متن خبر:
{text}
"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "شما یک متخصص دسته‌بندی اخبار ورزشی فارسی هستید."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=20,
                temperature=0.1
            )
            
            category = response.choices[0].message.content
            if category:
                category = category.strip()
            else:
                category = "سایر ورزش‌ها"
            return category
            
        except Exception as e:
            logger.error(f"Error categorizing news: {e}")
            return "سایر ورزش‌ها"

    async def generate_news_keywords(self, text: str) -> list:
        """Extract keywords from Persian news text"""
        try:
            prompt = f"""
لطفاً کلمات کلیدی مهم از متن خبری فارسی زیر استخراج کنید.
پاسخ را به صورت JSON با فرمت زیر ارائه دهید:
{{"keywords": ["کلمه1", "کلمه2", "کلمه3"]}}

متن:
{text}
"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "شما یک استخراج‌کننده کلمات کلیدی از متن فارسی هستید."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=100,
                temperature=0.2
            )
            
            content = response.choices[0].message.content
            if content:
                result = json.loads(content)
            else:
                raise Exception("No content received")
            return result.get("keywords", [])
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []

    async def ask_ai_about_esteghlal(self, question: str) -> str:
        """AI assistant for Esteghlal football team questions"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "تو یک کارشناس فوتبال مخصوص تیم استقلال هستی. اطلاعات کاملی از تاریخ، بازیکنان، مربیان و رکوردهای این تیم داری."
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content
            if answer:
                return answer.strip()
            else:
                return "متأسفانه نتوانستم به سوال شما پاسخ دهم."
                
        except Exception as e:
            logger.error(f"Error asking AI about Esteghlal: {e}")
            return "خطا در دریافت پاسخ از هوش مصنوعی."
