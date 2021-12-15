import scrapy
from re import search, match

class QuotesSpider(scrapy.Spider):
    name = "societies"

    def start_requests(self):

        with open("societies.csv", "w") as f:
                f.write(f'Name,Category,ID')
        with open("committees.csv", "w") as f:
                f.write(f'Name,Position,ID')
        with open("memberships.csv", "w") as f:
                f.write(f'Name,Price,ID')

        urls = [
            'https://engage.luu.org.uk/groups'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for new_link in response.xpath("//a/@href"):
            if search("https?:\/\/(www\.)?engage\.luu\.org\.uk\/groups\/[A-Z0-9]+\/[\w-]+(\/committee)?$",new_link.get()):
                print(new_link.get())
                yield response.follow(new_link, callback=self.parse)
        
        if search("https?:\/\/(www\.)?engage\.luu\.org\.uk\/groups\/[A-Z0-9]+\/[\w-]+$",response.url):
            
            societyName = response.xpath("//title[1]/text()").get()
            societyCategory = search("(?<=</svg>)[ \n]+([\w]+)", response.xpath("//header[@name='group-header']//p").get()).group(1)
            societyId = search("(?<=https:\/\/engage\.luu\.org\.uk\/groups\/)([A-Z0-9]+)(?=\/[\w-]+)", response.url).group(1)
            with open("societies.csv", "a") as f:
                f.write(f'\n"{societyName}","{societyCategory}","{societyId}"')

        elif search("https?:\/\/(www\.)?engage\.luu\.org\.uk\/groups\/[A-Z0-9]+\/[\w-]+\/committee$",response.url):
            positions = response.xpath("//li/div/div")
            societyId = search("(?<=https:\/\/engage\.luu\.org\.uk\/groups\/)([A-Z0-9]+)(?=\/[\w-]+)", response.url).group(1)
            
            with open("committees.csv", "a") as f:
                for position in positions:
                    occupantName = position.xpath(".//h4/text()").get()
                    positionName = position.xpath(".//p/text()").get()
                    f.write(f'\n"{occupantName}","{positionName}","{societyId}"')