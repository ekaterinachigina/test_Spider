import scrapy
import unicodedata


class CianSpiderSpider(scrapy.Spider):
    name = "cian_spider"
    allowed_domains = ["kazan.cian.ru"]
    start_urls = [f"https://kazan.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={i}&region=4777&room1=1" for i in range(1, 40)]
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

    def parse(self, response):
        rows = response.xpath("//div[@class='_93444fe79c--container--kZeLu _93444fe79c--link--DqDOy']")
        if len(rows) > 0:
            print(rows)
            for row in rows:
                info_adress = row.xpath(".//div[@class='_93444fe79c--labels--L8WyJ']/a")
                if len(info_adress) > 0:
                    adress = []
                    for elem_adress in info_adress:
                        adress.append(elem_adress.xpath(".//text()").get())
                    adress = ", ".join(adress)
                    price = row.xpath(".//span[@data-mark='MainPrice']/span/text()").get()
                    price = unicodedata.normalize('NFKD', price).replace(" ", "").replace('₽', '')
                    yield {
                        'name': row.xpath(".//span[@data-mark='OfferTitle']/span/text()").get(),
                        'adress': adress,
                        'price': price,
                        'url': row.xpath(".//a/@href").get(),
                        'page': response.xpath("//li[@class='_93444fe79c--page--tTWIr']/button/span/text()").get()
                    }
                parse_url = response.xpath("//nav[@data-name='Pagination']/a/@href").extract_first()
                # parse_url = response.urljoin(parse_url)
                # print(parse_url)
                if parse_url:
                    yield scrapy.Request(parse_url, callback=self.parse)
