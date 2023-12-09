import sqlite3
import csv
from player import Player
class DbManager:

    def __init__(self):
        self.connection = sqlite3.connect("davrosclan.db")
    
    def insert_data_from_csv(self, csv_file):
        
        cursor = self.connection.cursor()
        self.connection.execute("BEGIN") # Start transaction
        try:
            # Open the CSV file and read its contents
            with open(csv_file, 'r') as file:
                csv_reader = csv.reader(file, delimiter = '\t')
                for row in csv_reader:
                    username = row[2]
                    tag = row[3]
                    kicked = True if row[4] == 'ESPULSO' else False
                    p = Player(tag, username)
                    p.kicked = kicked
                    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS players (
                            tag TEXT PRIMARY KEY,
                            username TEXT NOT NULL,
                            kicked BOOL
                        )
                    ''')
                    cursor.execute("INSERT INTO players (tag, username, kicked) VALUES (?, ?, ?)", (p.tag, p.username, p.kicked))
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"{e}")
        finally:
            cursor.close()
    
    def find_player_in_db(self, player_tag):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM PLAYERS WHERE tag = ?", [player_tag])
            row = cursor.fetchall()[0]
            if row is not None:
                p = Player(row[0], row[1])
                p.kicked = row[2]
                return p
            return None
        except Exception as e:
            print(f"{e}")
        finally:
            cursor.close()

    def load_not_kicked_players(self):
        cursor = self.connection.cursor()
        result = []
        try:
            cursor.execute("SELECT * FROM PLAYERS WHERE kicked = 0")
            rows = cursor.fetchall()
            for row in rows:   
                p = Player(row[0], row[1])
                p.kicked = row[2]
                result.append(p)
            return result
        except Exception as e:
            print(f"{e}")
        finally:
            cursor.close()
    
    def insert_player(self, player: Player):
        if player.tag is not None and player.tag != "" and player.username is not None and player.username != "":
            cursor = self.connection.cursor()
            self.connection.execute("BEGIN") # Start transaction
            try:
                cursor.execute("INSERT INTO players (tag, username, kicked) VALUES (?, ?, ?)", (player.tag, player.username, False))
                self.connection.commit()
            except Exception as e:
                self.connection.rollback()
                print(f"{e}")
            finally:
                cursor.close()
    
    def kick_player(self, player: Player):
        if player.tag is not None and player.tag != "" and player.username is not None and player.username != "":
            cursor = self.connection.cursor()
            self.connection.execute("BEGIN") # Start transaction
            try:
                cursor.execute("UPDATE players SET kicked = 1 WHERE tag = ?", [player.tag])
                self.connection.commit()
            except Exception as e:
                self.connection.rollback()
                print(f"{e}")
            finally:
                cursor.close()
    
    def unkick_player(self, tag):
        if tag is not None and tag != "":
            cursor = self.connection.cursor()
            self.connection.execute("BEGIN") # Start transaction
            try:
                cursor.execute("UPDATE players SET kicked = 0 WHERE tag = ?", [tag])
                self.connection.commit()
            except Exception as e:
                self.connection.rollback()
                print(f"{e}")
            finally:
                cursor.close()
