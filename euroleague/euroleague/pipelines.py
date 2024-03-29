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

    def close_spider(self, spider):
        # finalize output files
        self.file_players.write("]\n")
        self.file_players.close() 
        self.file_teams.write("]\n")
        self.file_teams.close() 

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        # Based on item type we choose to which file to write
        if isinstance(item, Player): 
            self.file_players.write(line) 
        else:
            self.file_teams.write(line)        
        return item
