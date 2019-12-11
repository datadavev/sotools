from scrapy.spiders import SitemapSpider
import sotools
from pprint import pprint


'''
TODO:
- get date modified from sitemap
- generate system metadata
- preserve state to enable efficient re-harvest
'''
class SOBaseSpider(SitemapSpider):
    name = "sobase"
    sitemap_urls = ["https://www.archive.arm.gov/metadata/adc/sitemap.xml"]

    def __init__(self, *args, **kwargs):
        super(SOBaseSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        g = None
        try:
            g = sotools.loadSOGraphFromHtml(response.body, response.url)
        except Exception as e:
            self.logger.warning(e)
        self.logger.info(f"response url = {response.url} has a Dataset = {sotools.isDataset(g)}")
        identifiers = sotools.getDatasetIdentifiers(g)
        print(str(identifiers))
        metadata = sotools.getDatasetMetadataLinks(g)
        res = {
            "source": response.url,
            "identifiers": identifiers,
            "metadata": metadata
        }
        yield res
        #for identifier in identifiers:
        #    yield identifier
