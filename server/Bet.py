from User import User
from Game import Game
import uuid
from datetime import datetime
from database import database


def generate_uuid():
    return str(uuid.uuid4())


class Bet:
    def __init__(
            self,
            game_id: str,
            user: User,
            amount: int,
            bet_nums: list,
            id: str = generate_uuid(),
            create_time=datetime.now()
    ) -> None:
        self.id = id
        self.create_time = create_time
        self.game_id = game_id
        self.user = user
        self.bet_nums = bet_nums
        self.amount = amount

    def __str__(self) -> str:
        time = self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        return f"id: {self.id}, create_time: {time}, user: {self.user.username}, game_id: {self.game_id}, bet_nums: {self.bet_nums}, amount: {self.amount}"

    def save_to_db(self) -> str:
        try:
            result = database.db.execute("INSERT INTO Bet VALUES (?, ?, ?, ?, ?, ?)", (
                self.id,  self.create_time, self.game_id, self.user.username, str(self.bet_nums), self.amount))
        except Exception as e:
            result = e
        print(result)
        return result


if __name__ == "__main__":
    user = User("test")
    game = Game("123")
    bet = Bet(game.id, user, 100, [1, 2, 3])
    database.db.create_table()
    print(bet)
    bet.save_to_db()
