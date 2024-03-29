# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import json
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from euroleague.items import Player, Team


class EuroleaguePipeline:

    def open_spider(self, spider):
        # create output files
        self.file_players = open("players.json", "w")
        self.file_players.write("[\n")  
        self.file_teams = open("teams.json", "w")
        self.file_teams.write("[\n")  
        self.players = []
        self.teams = []

    def close_spider(self, spider):
        # finalize output files
        # write all players as json and separate each line with comma and new line 
        player_lines = [
            "\t" + json.dumps(ItemAdapter(p).asdict())
            for p in self.players
        ]
        player_lines_joined = ",\n".join(player_lines)
        self.file_players.write(player_lines_joined)
        self.file_players.write("\n]\n")
        # write all teams as json and separate each line with comma and new line 
        team_lines = [
            "\t" + json.dumps(ItemAdapter(t).asdict())
            for t in self.teams
        ]
        team_lines_joined = ",\n".join(team_lines)
        self.file_teams.write(team_lines_joined)
        self.file_teams.write("\n]\n")
        self.file_teams.close() 

    def process_item(self, item, spider):
        # Based on item type we store the items
        if isinstance(item, Player): 
            self.players.append(item)
        else:
            self.teams.append(item)     
        return item
