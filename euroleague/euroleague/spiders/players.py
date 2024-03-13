import scrapy
import re


class PlayersSpider(scrapy.Spider):
    name = "players"
    allowed_domains = ["www.euroleaguebasketball.net"]
    start_urls = ["https://www.euroleaguebasketball.net"]

    def start_requests(self):
        urls = [
            # "https://www.euroleaguebasketball.net/en/euroleague/players/sterling-brown/012720/",
            # "https://www.euroleaguebasketball.net/en/euroleague/players/shane-larkin/007200/",
            # "https://www.euroleaguebasketball.net/en/euroleague/players/marko-guduric/004004/",
            # "https://www.euroleaguebasketball.net/en/euroleague/players/yam-madar/011052/",
            # "https://www.euroleaguebasketball.net/en/euroleague/players/melih-mahmutoglu/002969/",
            "https://www.euroleaguebasketball.net/en/euroleague/teams/fenerbahce-beko-istanbul/roster/ulk/?season=2023-24"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_team)

    def parse_team(self, response):
        body = str(response.body)
        matches = re.findall('url":"/en/euroleague/players/.*?"', body)
        for match in matches:
            player_page = response.urljoin(match[6:-1])
            yield scrapy.Request(player_page, callback=self.parse_player)
        
    def parse_player(self, response):
        player = {}
         
        player["first_name"] = response.css(".hero-info_firstName__j_EvX::text").get()
        player["last_name"] = response.css(".hero-info_lastName___ngTo::text").get()
        groups = response.css(".stats-table_row__ttfiG")
        for i, group in enumerate(groups):
            data_cells = group.css(".stats-table_cell__hdmqc::text").getall()
            if i == 10 and len(data_cells) == 5:
                player["total_minutes"] = data_cells[0]
                player["total_points"] = data_cells[1]
                player["pt2_made_attempt"] = data_cells[2]
                player["pt3_made_attempt"] = data_cells[3]
                player["fg_made_attempt"] = data_cells[4]
            if i == 14 and len(data_cells) == 3:
                player["rebounds_OFF"] = data_cells[0]
                player["rebounds_DEF"] = data_cells[1]
                player["rebounds_TOT"] = data_cells[2]

        yield player