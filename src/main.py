import discord
import re
import os
from coc_service import CocService
from db_manager import DbManager
from player import Player

class CommandLineInterface(discord.Client):

    DISCORD_API_TOKEN = os.environ.get("DISCORD_API_TOKEN")

    SYNC_MEMBER_LIST_CMD = "DC!SYNC"
    FIX_MEMBER = "DC!FIX"

    def is_admin(self, roles):
        for role in roles:
            if str(role).upper() == 'ADMIN':
                return True
        return False
    
    def contains_player(self, player: Player, lst:[]):
        if len(lst) > 0:
            for i in lst:
                if player.tag == i.tag:
                    return True
        return False


    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        log_list = []
        if not self.is_admin(message.author.roles) or message.author == self.user:
            return
        else:
            if message.content == 'ping':
                await message.channel.send('pong')
            elif str(message.content).upper() == CommandLineInterface.SYNC_MEMBER_LIST_CMD:
                try:
                    coc_service = CocService()
                    newest_players = coc_service.get_player_list("#VLL2CUVJ")
                    db = DbManager()
                    # Looking for new players or return
                    for new_player in newest_players:
                        old_player = db.find_player_in_db(new_player.tag)
                        if old_player is None:
                            db.insert_player(new_player)
                            log_list.append(f"{new_player.username}({new_player.tag}) -> (NEW)")
                        else:
                            if old_player.kicked == True:
                                log_list.append(f"{new_player.username}({new_player.tag}) = (IS BACK)")
                    # Looking for players left from clan
                    current_active_players = db.load_not_kicked_players()
                    if len(current_active_players) > 0:
                        for op in current_active_players:
                            if self.contains_player(op, newest_players) == False:
                                # update the row
                                db.kick_player(op)
                                log_list.append(f"{op.username}({op.tag}) <- (LEFT)")
                    # Write the log
                    if len(log_list) > 0:
                        result_string = "\n".join(log_list) 
                    else:
                        result_string = "There aren't alarms :)"
                    await message.channel.send(f"{result_string}")    
                except Exception as e:
                    await message.channel.send(f"Error {e}")
            elif str(message.content).upper().find(CommandLineInterface.FIX_MEMBER) != -1:
                try:
                    db = DbManager()
                    hashtags = re.findall(r'#(\w+)', message.content)
                    for tag in hashtags:
                        db.unkick_player("#" + tag)
                        log_list.append(f"{tag} restored")
                    # Write the log
                    if len(log_list) > 0:
                        result_string = "\n".join(log_list) 
                    else:
                        result_string = "There aren't alarms :)"
                    await message.channel.send(f"{result_string}")
                except Exception as e:
                    await message.channel.send(f"Error {e}")
            else:
                await message.channel.send(f"Command {message.content} not implemented")
intents = discord.Intents.default()
intents.message_content = True
client = CommandLineInterface(intents=intents)
client.run(CommandLineInterface.DISCORD_API_TOKEN)