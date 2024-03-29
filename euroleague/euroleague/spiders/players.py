import json
import scrapy
import re


from euroleague.items import Player, Team


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
        for i, roster_link in enumerate(links):
            # roster link and team stats page link is similar
            # so we convert a roster link to a stats page link
            tokens = roster_link.split("/")
            tokens[5] = "statistics"
            tokens[7] = "?season=2023-24&phase=All%20phases#average"
            stats_link = "/".join(tokens)  
            # follow both links for each team by using different parse methods
            yield response.follow(roster_link, callback=self.parse_team_roster)
            yield response.follow(stats_link, callback=self.parse_team_stats)
            # Comment out this part while testing things, so number of pages scraped is lower
            # if i == 0:
            #     break

    def parse_team_stats(self, response):
        # We create a Team object to be populated
        team = Team()
        # Populate team name
        h1_text =  response.css(".club-info_name__xB4rz::text").get()
        position = h1_text.find("<")
        if position != -1:
            team.team_name = h1_text[0:position] 
        else:
            team.team_name = h1_text
        # this element is a script tag with json data
        # so we read the json and then extract data from the relevant bits 
        page_data = response.css("#__NEXT_DATA__::text").get() 
        page_data = json.loads(page_data)
        groups = page_data["props"]["pageProps"]["teamStats"][0]["groups"]
        average_stats = groups[0]["stats"]
        for average_stat in average_stats:
            stat_name = average_stat["name"]
            stat_value = average_stat["value"][0]["statValue"]
            team.averages[stat_name] = stat_value
        total_stats = groups[1]["stats"]
        for total_stat in total_stats:
            stat_name = total_stat["name"]
            stat_value = total_stat["value"][0]["statValue"]
            team.totals[stat_name] = stat_value
        # Return Team object so it can be processed further
        yield team
        
    def parse_team_roster(self, response):
        body = str(response.body)
        matches = re.findall('url":"/en/euroleague/players/.*?"', body)
        for i, match in enumerate(matches):
            player_page = response.urljoin(match[6:-1])
            yield scrapy.Request(player_page, callback=self.parse_player)
            # Comment out this part while testing things, so number of pages scraped is lower
            # if i == 5:
            #     break
        
    def parse_player(self, response):
        # We create a Player object to be populated
        player = Player()
        player.first_name = response.css(".hero-info_firstName__j_EvX::text").get()
        player.last_name = response.css(".hero-info_lastName___ngTo::text").get()
        groups = response.css(".stats-table_row__ttfiG")
        stats = {}
        for i, group in enumerate(groups):
            data_cells = group.css(".stats-table_cell__hdmqc::text").getall()
            if i == 10 and len(data_cells) == 5:
                stats["total_minutes"] = data_cells[0]
                stats["total_points"] = data_cells[1]
                stats["pt2_made_attempt"] = data_cells[2]
                stats["pt3_made_attempt"] = data_cells[3]
                stats["fg_made_attempt"] = data_cells[4]
            if i == 14 and len(data_cells) == 3:
                stats["rebounds_OFF"] = data_cells[0]
                stats["rebounds_DEF"] = data_cells[1]
                stats["rebounds_TOT"] = data_cells[2]
        player.stats = stats
        # Return Player object so it can be processed further
        yield player