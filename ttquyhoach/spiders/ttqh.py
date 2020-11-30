import scrapy
import json

class TtqhSpider(scrapy.Spider):
    name = 'ttqh'
    #allowed_domains = ['thongtinquyhoach.hochiminhcity.gov.vn']
    start_urls = ['https://sqhkt-qlqh.tphcm.gov.vn/api/quan-huyen']

    check = False

    def parse(self, response):
        base_url = 'https://sqhkt-qlqh.tphcm.gov.vn/api/phuong-xa/'
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Host": "sqhkt-qlqh.tphcm.gov.vn",
            "Origin": "https://thongtinquyhoach.hochiminhcity.gov.vn",
            "Referer": "https://thongtinquyhoach.hochiminhcity.gov.vn/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
        }
        data = json.loads(response.body)
        for district in data:
            url = base_url + str(district['maquanhuyen'])
            yield scrapy.Request(url=url, callback=self.parse_ward, headers=headers, meta={"tenquanhuyen":district['tenquanhuyen']})
    
    def parse_ward(self, response):
        url = 'https://sqhkt-qlqh.tphcm.gov.vn/computing/930/api/v3.1/a-z/all'
        data = json.loads(response.body)
        # soto = 200
        soto = 2
        sothua = 51
        for ward in data:
            for i in range(1,soto):
                self.check = False
                for j in range(1,sothua):    
                    mathuadat = ward['maphuongxa'] + str(i).zfill(3) + str(j).zfill(4)
                    if self.check: break
                    yield scrapy.FormRequest(url, method='POST', callback=self.parse_detail, formdata={"MaThuaDat": mathuadat})
                    #self.log(type(res))
                    # yield {
                    #     "maphuongxa": ward['maphuongxa'],
                    #     "tenphuongxa": ward['tenphuongxa'],
                    #     "maquanhuyen": ward['maquanhuyen'],
                    #     "tenquanhuyen": response.meta.get("tenquanhuyen")
                    # }
                    # yield {
                    #     "MaThuaDat": mathuadat
                    # }
                    
    def parse_detail(self, response):
        data = json.loads(response.body)
        if response.body=='' or response.body == None: 
            self.check = True
            return

        yield data

