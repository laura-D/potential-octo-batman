from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy import log
from Crawler.items import ListItem, MetaItem, DownItem
from pymongo import MongoClient
from scrapy import log
from scrapy.http import Request
from bson.objectid import ObjectId

class pc6Spider(BaseSpider):
	name = 'pc6Spider'
	allowed_domains = ['www.pc6.com']

	modeList = ['list', 'meta', 'down']
	mode = modeList[0]

	inited = False

	def __init__(self, mode, *args, **kwargs):
		super(AnzhiSpider, self).__init__(*args, **kwargs)
		self.start_urls = []

		if mode not in self.modeList:
			mode = self.modeList[0]
		self.mode = mode

		if self.mode == 'list':
			self.start_urls.append('http://www.pc6.com/android/588_1.html')
		elif self.mode == 'meta':
			client = MongoClient()
			db = client.meta_crawler
			listItems = db.list_items
			for oneItem in listItems.find():
				self.start_urls.append(oneItem['url'])
		elif self.mode == 'down':
			self.start_urls.append('http://www.pc6.com/android/588_1.html')

	def parse(self,response):
		sel = Selector(response)

		if self.mode == self.modeList[0]:
			nextRetUrl =  ''.join(sel.xpath('//a[@class="tsp_next"]/@href').extract())
			if nextRetUrl != []:
				yield Request('http://www.pc6.com' + nextRetUrl, callback = self.parse)

			for url in sel.xpath('//dd[@class="rmain"]/ul/li/a/@href').extract():
				listItem = ListItem()
				listItem['mode'] = self.mode
				listItem['market'] = 'pc6'
				listItem['url'] = 'http://www.pc6.com' + url
				yield listItem

		elif self.mode == 'meta':
			metaItem = MetaItem()
			metaItem['mode'] = self.mode
			metaItem['market'] = 'pc6'
			metaItem['url'] = response.url
			metaItem['title'] = sel.xpath('//div[@class="fixed"]/h1/text()').extract()
			metaItem['version'] = ''
			metaItem['desc'] = sel.xpath('//div[@id="content"]/p/text()').extract()

			yield metaItem
		elif self.mode == 'down':
			if self.inited == False:
				self.inited = True
				client = MongoClient()
				db = client.meta_crawler
				downItems = db.down_items
				metaItems = db.meta_items
				for oneItem in downItems.find({}, {'pc6':1, '_id':0}):
					for oneId in oneItem['pc6']:
						result = metaItems.find_one({'_id': ObjectId(oneId)}, {'url':1, '_id':0})
						request = Request(result['url'], callback = self.parse)
						request.meta['oid'] = oneId
						yield request
			else:
				downItem = DownItem()
				downItem['mode'] = self.mode
				downItem['url'] = sel.xpath('//a[@class="zs91"]/@href').extract()
				downItem['oid'] = response.meta['oid']
				yield downItem


