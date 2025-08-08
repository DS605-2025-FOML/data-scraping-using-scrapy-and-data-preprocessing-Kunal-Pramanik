import scrapy
from ..items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"  # Unique name for the spider
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        all_div_quotes = response.css('div.quote')

        for quote_div in all_div_quotes:
            # Create new item for each quote
            items = QuoteItem()

            text = quote_div.css('span.text::text').get()
            author = quote_div.css('.author::text').get()
            tags = quote_div.css('.tag::text').getall()

            items['text'] = text
            items['author'] = author
            items['tags'] = tags

            yield items

        # pagination
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
