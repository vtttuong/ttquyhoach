import scrapy
import json

class TtqhSpider(scrapy.Spider):
    name = 'ttqh1'
    check = False

    def start_requests(self, response):
        base_url = 'https://sqhkt-qlqh.tphcm.gov.vn/computing/930/api/v3.1/a-z/all'
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
        # soto = 200
        soto = 2
        sothua = 51
        for i in range(1,soto):
            self.check = False
            for j in range(1,sothua):    
                mathuadat = '26740' + str(i).zfill(3) + str(j).zfill(4)
                if self.check: break
                yield scrapy.FormRequest(base_url, method='POST', headers=headers, callback=self.parse_detail, formdata={"MaThuaDat": mathuadat})

                    
    def parse_detail(self, response):
        data = json.loads(response.body)
        if response.body=='' or response.body == None: 
            self.check = True
            return
        yield data

