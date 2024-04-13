

import sqlite3

class DB_bio:
    def __init__(self,name_base:str):
        self.name_base = name_base


    def connect (self):
       self.connection = sqlite3.connect(self.name_base)
       self.cursor = self.connection.cursor()


    def execute_bio(self, human, bio):

        self.cursor.execute('INSERT INTO Users (human, biography) VALUES (?, ?)',
                       (f'{human}', f'{bio}'))

        self.connection.commit()