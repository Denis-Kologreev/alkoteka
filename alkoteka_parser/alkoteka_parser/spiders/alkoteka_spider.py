import scrapy
import json
from ..items import AlkotekaItem
from datetime import datetime


class AlkotekaSpider(scrapy.Spider):
    name = 'alkoteka_spider'
    allowed_domains = ['alkoteka.com']
    start_urls = [
        "https://alkoteka.com/catalog/slaboalkogolnye-napitki-2",
    ]

    def __init__(self, cookies_file=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cookies = {}

        if cookies_file:
            try:
                # фйал с куками для региональности
                with open(f'./alkoteka_parser/result.json', 'r', encoding='utf-8') as f:
                    self.cookies = json.load(f)
            except Exception as e:
                self.logger.error(f"Ошибка при чтении файла куков: {e}")

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_category,
                cookies=self.cookies,
                meta={'js': True},
                dont_filter=True
            )

    # Остальной код (parse_category, parse_product и т.д.) остается без изменений


    def parse_category(self, response):
        self.logger.info(f"Парсим категорию: {response.url}")

        # Ссылки на товары (xpath)
        product_links = response.xpath('//div[contains(@class, "card-product")]//a/@href').getall()

        if not product_links:
            self.logger.warning("Нет товаров на странице")
            return

        for link in product_links:
            full_url = response.urljoin(link)
            yield scrapy.Request(
                url=full_url,
                callback=self.parse_product,
                meta={'js': True}
            )

        # Переход на следующую страницу (xpath)
        next_page = response.xpath('//a[@class="pagination__next"]/@href').get()
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse_category,
                meta={'js': True}
            )

    def parse_product(self, response):
        self.logger.info(f"Парсим товар: {response.url}")

        item = AlkotekaItem()

        # Обязательные поля (xpath)
        item['RPC'] = response.xpath('//span[@class="product-id"]/text()').get(default='N/A')
        item['url'] = response.url
        item['title'] = response.xpath('//h1[@class="product-title"]/text()').get(default='Без названия')
        item['marketing_tags'] = response.xpath('//div[@class="product-tags"]//span/text()').getall()
        item['brand'] = response.xpath('//div[@class="product-brand"]/text()').get(default='Не указано')

        # Цена и скидка (xpath)
        current_price_text = response.xpath('//span[@class="price-current"]/text()').get()
        original_price_text = response.xpath('//span[@class="price-original"]/text()').get()

        try:
            current_price = float(current_price_text.replace(' ', '').replace('₽', '')) if current_price_text else 0.0
        except Exception as e:
            current_price = 0.0
            self.logger.warning(f"Ошибка при парсинге цены: {e}")

        try:
            original_price = float(original_price_text.replace(' ', '').replace('₽', '')) if original_price_text else 0.0
        except Exception as e:
            original_price = 0.0
            self.logger.warning(f"Ошибка при парсинге оригинальной цены: {e}")

        sale_tag = None
        if current_price < original_price and original_price > 0:
            discount_percentage = round((original_price - current_price) / original_price * 100)
            sale_tag = f"Скидка {discount_percentage}%"

        item['price_data'] = {
            'current': current_price,
            'original': original_price,
            'sale_tag': sale_tag
        }

        # Наличие (xpath)
        in_stock = len(response.xpath('//span[@class="in-stock" and contains(text(), "В наличии")]')) > 0
        stock_count = int(response.xpath('//span[@class="stock-count"]/text()').get() or 0)

        item['stock'] = {
            'in_stock': in_stock,
            'count': stock_count
        }

        # Изображения (xpath)
        item['assets'] = {
            'main_image': response.xpath('//img[@class="product-main"]/@src').get(),
            'set_images': response.xpath('//div[@class="gallery"]//img/@src').getall(),
            'view360': [],
            'video': []
        }

        # Характеристики (xpath)
        metadata = {'__description': response.xpath('//div[@class="product-description"]/text()').get()}
        specs = response.xpath('//table[@class="specs"]//tr')

        for spec in specs:
            key = spec.xpath('.//td[1]/text()').get()
            val = spec.xpath('.//td[2]/text()').get()
            if key and val:
                metadata[key.strip()] = val.strip()

        item['metadata'] = metadata
        item['variants'] = len(response.xpath('//div[@class="variants"]//option'))

        # Таймстамп
        item['timestamp'] = int(datetime.now().timestamp())

        yield item
