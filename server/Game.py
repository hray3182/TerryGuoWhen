import datetime
import random
from database import database
import json
import User
import Bet

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

    @classmethod
    def get_num_of_todays_game(cls) -> int:
        today = datetime.datetime.now().date().strftime("%Y-%m-%d")
        count = 0
        try:
            # result = database.db.execute("SELECT COUNT(*) FROM Game WHERE create_time LIKE ?", (f"{today}%",))
            result = database.db.execute("SELECT COUNT(*) FROM Game WHERE DATE(create_time) = ?", (today,))
            count = int(result[0][0])
            # result = result.fetchone()[0]
        except Exception as e:
            result = e
            return result
        return count



class GameManager():
# A game lasts one munite, 40 second to accept bets, 10 second to count, 10 second to announce the result
    def __init__(self) -> None:
        # game id should be like 
        todays_count = Game.get_num_of_todays_game()
        # game id should be like yyyy-mm-dd-0001
        today = datetime.datetime.now().date().strftime("%Y-%m-%d")
        self.current_game = Game(f"{today}-{todays_count + 1}")
        self.stop_bet_time = self.current_game.create_time + datetime.timedelta(seconds=40)
        self.current_game_state = 0
        self.bets: list[Bet.Bet] = []
            
    def __str__(self) -> str:
        return f"Current game: {self.current_game}, stop bet time: {self.stop_bet_time}"

    
    def json(self):
        def handler(o):
            if isinstance(o, datetime.datetime):
                return o.isoformat()
            else: 
                return o.__dict__
        return json.dumps(self, default=handler)

    def create_next_game(self):
        today = datetime.datetime.now().date().strftime("%Y-%m-%d")
        todays_count = Game.get_num_of_todays_game()
        self.current_game = Game(f"{today}-{todays_count + 1}")
        self.stop_bet_time = self.current_game.create_time + datetime.timedelta(seconds=2) # 先用 2 秒測試
        
    def message_for_client(self):
        # json format
        return {
            "game_id": self.current_game.id,
            "game_state": self.current_game_state,
            "user": None,
            "current_bets": [],
            "earn": None
        }




if __name__ == "__main__":
    database.db.create_table()
    
    # Game("123").save_to_db()
    # Game("456").save_to_db()

    # print(Game.get_num_of_todays_game())
    print(GameManager().json())