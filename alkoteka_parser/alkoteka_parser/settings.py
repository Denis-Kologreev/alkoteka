# alkoteka_parser/settings.py

BOT_NAME = 'alkoteka_parser'

SPIDER_MODULES = ['alkoteka_parser.spiders']
NEWSPIDER_MODULE = 'alkoteka_parser.spiders'

# Логирование и кодировка
LOG_LEVEL = 'ERROR'
FEED_EXPORT_ENCODING = 'utf-8'

# Настройки заголовков и User-Agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'

# Отключаем кэширование по умолчанию
HTTPCACHE_ENABLED = False

# Настройки middleware
DOWNLOADER_MIDDLEWARES = {
    'alkoteka_parser.middlewares.SeleniumMiddleware': 543,
}
