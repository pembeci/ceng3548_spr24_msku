import scrapy


class LetterboxSpider(scrapy.Spider):
    name = "letterboxd"
    allowed_domains = ["letterboxd.com"]
    start_urls = [
        "https://letterboxd.com/film/monkey-man/crew/",
        "https://letterboxd.com/film/sasquatch-sunset/",
        "https://letterboxd.com/film/girls-state/",
        "https://letterboxd.com/film/the-great-escape/"
    ]

    def parse(self, response):
        movie = {}
        tab_cast = response.css("#tab-cast")
        links = tab_cast.css("p a")
        cast = []
        for link in links:
            cast_item = {}
            cast_item["name"] = link.css("::text").get()
            cast_item["page"] = link.attrib["href"]
            cast_item["title"] = link.attrib.get("title", "")
            cast.append(cast_item)
        movie["cast"] = cast
        film_header = response.css("#featured-film-header")
        movie["title"] = film_header.css("h1::text").get()
        movie["year"] = film_header.css("small > a::text").get()
        movie["director"] = film_header.css("p > a > span::text").get()
        return movie

