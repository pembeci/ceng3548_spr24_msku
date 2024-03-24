import json
import scrapy
import re


class PlayersSpider(scrapy.Spider):
    name = "players"
    allowed_domains = ["www.euroleaguebasketball.net"]
    start_urls = ["https://www.euroleaguebasketball.net"]
    # scrapy crawl players -o players_w5.json
    def start_requests(self):
        urls = [
            "https://www.euroleaguebasketball.net/en/euroleague/teams/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_teams)
            

    def parse_teams(self, response):
        links = response.css("a.teams-card_card__HH6Mn::attr(href)").getall()
        for roster_link in links:
            # roster link and team stats page link is similar
            # so we convert a roster link to a stats page link
            tokens = roster_link.split("/")
            tokens[5] = "statistics"
            tokens[7] = "?season=2023-24&phase=All%20phases#average"
            stats_link = "/".join(tokens)  
            # follow both links for each team by using different parse methods
            yield response.follow(roster_link, callback=self.parse_team_roster)
            yield response.follow(stats_link, callback=self.parse_team_stats)

    def parse_team_stats(self, response):
        team = {"averages": {}, "total": {}}
        # this element is a script tag with json data
        # so we read the json and then extract data from the relevant bits 
        page_data = response.css("#__NEXT_DATA__::text").get() 
        page_data = json.loads(page_data)
        groups = page_data["props"]["pageProps"]["teamStats"][0]["groups"]
        average_stats = groups[0]["stats"]
        for average_stat in average_stats:
            stat_name = average_stat["name"]
            stat_value = average_stat["value"][0]["statValue"]
            team["averages"][stat_name] = stat_value
        total_stats = groups[1]["stats"]
        for total_stat in total_stats:
            stat_name = total_stat["name"]
            stat_value = total_stat["value"][0]["statValue"]
            team["total"][stat_name] = stat_value
            print(stat_name, stat_value)
        # store team dictionary as an item
        yield team
        
    def parse_team_roster(self, response):
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