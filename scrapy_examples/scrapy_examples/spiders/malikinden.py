import scrapy


class MalikindenSpider(scrapy.Spider):
    name = "malikinden"
    allowed_domains = ["malikinden.com"]
    start_urls = [
        "https://malikinden.com/ilan/emlak-konut-satilik-daire-izmir-karsiyaka-yali-da-satilik-31-lux-daire/4375/detay",
        "https://malikinden.com/ilan/emlak-konut-kiralik-daire-bogaz-manzarali-terasli-21-kiralik-daire-moda/4883/detay",
        "https://malikinden.com/ilan/emlak-konut-satilik-daire-karanlik-odasiz-cift-cephe-31/4857/detay",
    ]

    def parse(self, response):
        ad = {}
        items = response.css(".adAttributes li")
        for item in items:
            divs = item.css("div::text")
            if len(divs) == 0:
                continue
            ad_field_title = divs[0].get()
            if len(divs) == 1:
                font_tag = item.css("font::text")
                ad_field_val = font_tag.get()
            else:
                ad_field_val = divs[1].get()    
            ad_field_val = ad_field_val.replace("\n", "")  
            ad_field_val = ad_field_val.strip()
            ad[ad_field_title] =  ad_field_val
        return ad                
        