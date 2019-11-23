from scrapy.spiders import SitemapSpider
import sotools
from pprint import pprint

class SOBaseSpider(SitemapSpider):
    name = "sobase"
    sitemap_urls = ["https://www.archive.arm.gov/metadata/adc/sitemap.xml"]

    def __init__(self, *args, **kwargs):
        super(SOBaseSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        g = None
        try:
            g = sotools.loadJsonLdGraphFromHtml(response.body, response.url)
        except Exception as e:
            self.logger.warning(e)
        self.logger.info(f"response url = {response.url} has a Dataset = {sotools.isDataset(g)}")
        identifiers = sotools.getDatasetIdentifiers(g)
        print(str(identifiers))
        #for identifier in identifiers:
        #    yield identifier
