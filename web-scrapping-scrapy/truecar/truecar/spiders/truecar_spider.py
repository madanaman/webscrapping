import scrapy

class TrueCar(scrapy.Spider):
    name = "truecar"


    def start_requests(self):
        urls = ['https://www.marutisuzukitruevalue.com/buy-car/1#listingCity=New&CarCityRange=50&page=1&modeltype=ignis&varientType=ignis%3A&transmissionType=automatic&fuelType=petrol&certifiedCars=true']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        # all_listings = response.xpath(".//*[@class='carBox']")
        # response.xpath(".//*[@class='carBox']").getall()
        # all_listings = response.xpath(".//div[@class='carBox']/div[@class='row']/div[@class='col-sm-12 col-12']")[1]\
        #     .xpath(".//div[@class='rightSection']")
        all_listings = response.xpath(".//div[@class='carBox']")

        for car in all_listings:
            car = car.xpath(".//div[@class='row']/div[@class='col-sm-12 col-12']")[1]\
                .xpath(".//div[@class='rightSection']")
            car_data = {
                'url': car.css('a::attr(href)').get(),
                'model': car.css('a::text').get(),
                'price': car.xpath(".//div[@class='priceSection']").css('span::text').get(),
                'year': car.xpath(".//div[@class='details']").css('ul > li').css('::text').get(),
                'Kms': car.xpath(".//div[@class='details']").css('ul > li')[2].css('::text').get(),
                'fuel': car.xpath(".//div[@class='details']").css('ul > li')[1].css('::text').get()
            }

            yield car_data

