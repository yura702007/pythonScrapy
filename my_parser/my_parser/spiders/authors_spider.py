import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'author'
    start_urls = ['https://quotes.toscrape.com/']

    def parse(self, response, **kwargs):
        author_page_link = response.css('.author + a')
        yield from response.follow_all(author_page_link, callback=self.parse_author)

        paginator_links = response.css('li.next a')
        yield from response.follow_all(paginator_links, callback=self.parse)

    @staticmethod
    def parse_author(response):
        def extract_with_css(query):
            return response.css(query).get().strip()
        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text')
        }
