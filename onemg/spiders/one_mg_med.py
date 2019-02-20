# -*- coding: utf-8 -*-
from scrapy.spiders import SitemapSpider
import json


class OneMgMedSpider(SitemapSpider):
    name = 'one_mg_med'
    allowed_domains = ['1mg.com']
    max_length = 24
    sitemap_urls = ["https://www.1mg.com/sitemap_drugs_{}.xml".format(i) for i in range(1, max_length + 1)]
    # sitemap_urls = sitemap_urls + [
    #     'https://www.1mg.com/sitemap_ayurveda_1.xml',
    # ]
    # sitemap_urls = sitemap_urls + [
    #     'https://www.1mg.com/sitemap_generics_1.xml',
    # ]

    print(sitemap_urls)

    def parse(self, response):
        pattern = "window.PRELOADED_STATE\s=\s\[(.*)];"
        script_text = response.xpath("normalize-space(.//script[contains(.,'window.PRELOADED_STATE = [')]/text())") \
            .re_first(pattern)
        if script_text:
            self.logger.info("<pattern {}> match".format(pattern))
            data = json.loads(eval(script_text))
            # print(type(data))
            # print(isinstance(data, dict))
            self.logger.info("converted into json keys <{}>".format(data.keys()))
            if isinstance(data, dict):
                if "drugPage" in data:
                    # print(data['drugPage'].keys())
                    drug_data = data['drugPage']['drugInfo']['sku']
                    drug_data['sku_type'] = "drug"
                    yield drug_data
                if "otcPage" in data:
                    # print(data['otcPage']['otcInfo']['skus'].keys())
                    otc_data = data['otcPage']['otcInfo']['skus']
                    otc_data['sku_type'] = "otc"
                    yield otc_data
