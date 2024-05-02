import datetime
import random
from database import database

class Game:
    def __init__(self, id: str, create_time=datetime.datetime.now()) -> None:
        self.id = id
        self.nums = []
        self.create_time = create_time
        self.__generate_nums()

    def __str__(self) -> str:
        return f"id: {self.id}, nums: {self.nums}"

    def __generate_nums(self):
        self.nums = (random.sample(range(1, 11), 3))

    def save_to_db(self) -> str:
        try:
            result = database.db.execute("INSERT INTO Game VALUES (?, ?, ?)", (
                self.id, self.create_time, str(self.nums)))
        except Exception as e:
            result = e
        print(result)
        return result

if __name__ == "__main__":
    game = Game("123")
    print(game)
    database.db.create_table()
    game.save_to_db()
    
