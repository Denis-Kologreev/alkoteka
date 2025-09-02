# alkoteka_parser/middlewares.py
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

class SeleniumMiddleware:
    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Запуск без GUI
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-background-networking")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-breakpad")
        chrome_options.add_argument("--disable-client-side-phishing-detection")
        chrome_options.add_argument("--disable-component-update")
        chrome_options.add_argument("--disable-domain-reliability")
        chrome_options.add_argument("--disable-features=AudioServiceOutOfProcess")
        chrome_options.add_argument("--disable-hang-monitor")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--enable-automation")
        chrome_options.add_argument("--metrics-recording-only")
        chrome_options.add_argument("--safebrowsing-disable-auto-update")
        chrome_options.add_argument("--use-mock-keychain")

        service = Service()  # ← Укажите путь к chromedriver
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def process_request(self, request, spider):
        if "js" in request.meta:
            self.driver.get(request.url)
            time.sleep(2)  # Подождите, пока загрузится JS
            return HtmlResponse(
                url=self.driver.current_url,
                body=self.driver.page_source,
                encoding='utf-8',
                request=request
            )
        return None

    def spider_closed(self, spider):
        self.driver.quit()
