import scrapy
from ..items import BookItem

class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        all_books = response.css('article.product_pod')

        for book in all_books:
            item = BookItem()
            item['title'] = book.css('h3 a::attr(title)').get()
            item['price'] = book.css('.price_color::text').get()
            item['rating'] = book.css('p.star-rating').attrib['class'].replace('star-rating', '').strip()
            item['availability'] = ''.join(book.css('p.instock.availability::text').getall()).strip()

            yield item

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
