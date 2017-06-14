# -*- coding: utf-8 -*-
import scrapy
import re
import time

class Stock_priceSpider(scrapy.Spider):
    name = 'Get_Stock_Price'
    def start_requests(self):
	stock = getattr(self, 'stock', None)
        url = 'http://stock.finance.sina.com.cn/hkstock/history/%s.html' % stock
	yield scrapy.Request(url, self.parse)

    def parse(self,response):
	Year = int(time.strftime('%Y'))
	for year in range(2001,Year+1):
	    for season in range(1,5):
		#print str(year),str(season)
		yield scrapy.http.FormRequest.from_response(response,
			formname='daily',
			formdata={'year':str(year),'season':str(season)},
			callback=self.parse_mypage)

    def parse_mypage(self, response):
	#print('I am here')
        price_table = response.css('.sub01_cc')
	dates = price_table.css('tr+ tr td:nth-child(1)').extract()
	close_prices = price_table.css('tr+ tr td:nth-child(2)').extract()
	changes = price_table.css('tr+ tr td:nth-child(3)').extract()
	change_rates = price_table.css('tr+ tr td:nth-child(4)').extract()
	volumns = price_table.css('tr+ tr td:nth-child(5)').extract()
	volumn_HKDs = price_table.css('tr+ tr td:nth-child(6)').extract()
	open_prices = price_table.css('tr+ tr td:nth-child(7)').extract()
	highs = price_table.css('tr+ tr td:nth-child(8)').extract()
	lows = price_table.css('tr+ tr td:nth-child(9)').extract()
	percentages = price_table.css('tr+ tr td:nth-child(10)').extract()

	extract_digit = re.compile('-?\d+.\d+')
	for date,close_price,change,change_rate,volumn,volumn_HKD,open_price,high,low,percentage in zip(dates,close_prices,changes,change_rates,volumns,volumn_HKDs,open_prices,highs,lows,percentages):
		
	    yield {
	    	'date' : extract_digit.search(date).group(),
	    	'close' : extract_digit.search(close_price).group(),
	    	'change' : extract_digit.search(change).group(),
	    	'change_rate' : extract_digit.search(change_rate).group(),
		'volumn' : extract_digit.search(volumn).group(),
		'volumn_HKD' : extract_digit.search(volumn_HKD).group(),
		'open_price' : extract_digit.search(open_price).group(),
		'high' : extract_digit.search(high).group(),
		'low' : extract_digit.search(low).group(),
		'percentage' : extract_digit.search(percentage).group(),

		}
