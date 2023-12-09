import os
import requests
from player import Player
class CocService:
    
    COC_API_TOKEN = os.environ.get("COC_API_TOKEN")
    
    def __init__(self):
        if CocService.COC_API_TOKEN is None:
            raise Exception("Please set the envirnoment variable COC_API_TOKEN with the COC token")
        self.headers = {"Authorization": f"Bearer {CocService.COC_API_TOKEN}"}
    
    def get_player_list(self, clan_tag: str):
        result = []
        url = "https://api.clashofclans.com/v1/clans"
        if clan_tag[0] == "#":
            clan_tag = clan_tag.replace("#", "%23")
        url = f"{url}/{clan_tag}"
        response = requests.get(url, headers = self.headers)
        if response.status_code == 200:
            data = response.json()
            for member in data["memberList"]:
                p = Player(member['tag'], member['name'])
                result.append(p)
            return result
        else:
            print(f"Error {response.text}")


