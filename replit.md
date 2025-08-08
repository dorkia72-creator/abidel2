# Overview

A focused Telegram bot that aggregates Esteghlal football club news from multiple RSS feeds and provides full article reading functionality. The bot fetches news specifically about Esteghlal from major Iranian sports news sources and allows users to read complete articles through web scraping.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Bot Framework
- **Telegram Bot Architecture**: Built using python-telegram-bot library with async/await patterns
- **Command Structure**: Implements /start command and callback query handlers for news browsing and full article reading
- **Message Flow**: Simple interface with single button to get Esteghlal news, then individual buttons to read full articles

## News Aggregation System
- **RSS Feed Integration**: Pulls from 5 major Persian sports news sources (Varzesh3, Tarafdari, Footballi, Metafootball, Khabarvarzeshi)
- **Concurrent Processing**: Uses aiohttp for async HTTP requests to fetch multiple RSS feeds simultaneously
- **Esteghlal Filtering**: Specifically filters news containing "استقلال" keyword from all sources
- **Web Scraping**: Uses BeautifulSoup to fetch full article content from original news sources

## Article Reading Service
- **Web Scraping**: Uses requests and BeautifulSoup for extracting full article content
- **Content Processing**: Extracts meaningful paragraphs and limits content to 3000 characters
- **Error Handling**: Graceful fallback when full article content cannot be retrieved

## Configuration Management
- **Environment-Based Config**: All sensitive data (API keys, tokens) managed through environment variables
- **Validation System**: Required configuration validation with error handling for missing credentials
- **Configurable Limits**: Adjustable parameters for news count, cache timeout, and refresh intervals

## Error Handling & Logging
- **Comprehensive Logging**: File and console logging with UTF-8 encoding support for Persian text
- **Exception Management**: Try-catch blocks around all external API calls with graceful degradation
- **Timeout Controls**: Configurable request timeouts to prevent hanging operations

# External Dependencies

## Third-Party Services
- **Telegram Bot API**: Core messaging platform integration requiring TELEGRAM_BOT_TOKEN
- **RSS Feeds**: Five Persian sports news sources (Varzesh3, Tarafdari, Footballi, Metafootball, Khabarvarzeshi)

## Python Libraries
- **python-telegram-bot**: Telegram bot framework for async operations
- **feedparser**: RSS feed parsing and content extraction
- **requests**: HTTP client for web scraping
- **beautifulsoup4**: HTML parsing for article content extraction
- **aiohttp**: Async HTTP client for concurrent RSS feed fetching

## Runtime Requirements
- **Python 3.7+**: Async/await support and modern Python features
- **Environment Variables**: TELEGRAM_BOT_TOKEN must be configured
- **Network Access**: Outbound HTTPS connections to Telegram and Persian news sites