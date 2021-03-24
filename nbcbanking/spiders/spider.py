import scrapy

from scrapy.loader import ItemLoader

from ..items import NbcbankingItem
from itemloaders.processors import TakeFirst


class NbcbankingSpider(scrapy.Spider):
	name = 'nbcbanking'
	start_urls = ['https://www.nbcbanking.com/news/']

	def parse(self, response):
		post_links = response.xpath('//a[@rel="bookmark"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="nav-previous"]//a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//article//text()[normalize-space() and not(ancestor::h1 | ancestor::div[@class="entry-meta"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="posted_on"]/text()').get()

		item = ItemLoader(item=NbcbankingItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
