# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import SitemapSpider, Rule
import json, os


class OnemgBotSpider(SitemapSpider):
    name = '1mgBot'
    allowed_domains = ['1mg.com']
    max_length = 2
    sitemap_urls = ["https://www.1mg.com/labs/sitemap_lab_test_{}.xml".format(i) for i in range(1, max_length)]

    print(sitemap_urls)
    # sitemap_rules = [
    #     "*/labs/*/diagnostic-centers/*/*"
    # ]

    def parse(self, response):
        pattern = "window.PRELOADED_STATE\s=\s\[(.*)];"
        script_text = response.xpath("normalize-space(.//script[contains(.,'window.PRELOADED_STATE = [')]/text())") \
            .re_first(pattern)
        # .extract_first()
        # print(script_text)

        if script_text:
            data = json.loads(eval(script_text))
            # print(type(data))
            # print(isinstance(data, dict))
            if isinstance(data, dict):
                with open("asddsad.json", "w") as f:
                    json.dump(data, f)
                data['url'] = response.url
                for inventory in data['test']['data']['inventories']:
                    lab = inventory['lab']
                    del lab['accreditation']
                    for test in inventory['tests']:
                        test.update(test['priceInfo'])
                        del test['priceInfo']
                        yield {
                            **lab,
                            **test,
                            'url': response.url
                        }
