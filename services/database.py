import sqlite3

class Dbfunk():
    def __init__(self):
        self.db = sqlite3.connect('userf.db')
        self.cursor = self.db.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS TGBOTDB (
            username TEXT,
            tag TEXT)""")
        self.db.commit()
        self.db.close()

    def add(self, user, frend):
        self.db = sqlite3.connect('userf.db')
        self.cursor = self.db.cursor()
        self.cursor.execute(f"INSERT INTO TGBOTDB VALUES ('{user}', '{frend}')")
        self.db.commit()
        self.db.close()
    
    def get_friends(self, user_id):
        self.db = sqlite3.connect('userf.db')
        self.cursor = self.db.cursor()
        self.cursor.execute(f"SELECT tag FROM TGBOTDB WHERE username = '{user_id}'")
        friends = [row[0] for row in self.cursor.fetchall()]
        self.db.close()
        return friends
    
dbobjeck = Dbfunk()