import tornado.web
import tornado.websocket
import tornado.ioloop
import asyncio
import Game
import datetime
import json
import hashlib
import User
import controller

gameManager = Game.GameManager()

class WsRequest:
    def __init__(self, action: str, username: str = None, data: dict = None) -> None:
        self.action = action
        self.data = data
        self.username = username


class GameWebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = {}

    def open(self):
        # when new client connects, add it to the client set
        self.clients[self] = {}
        self.clients[self]["is_verify"] = False
        self.write_message("連接成功")

    def on_close(self):
        # when client disconnects, remove it from the client set
        del self.clients[self]

    def on_message(self, msg):
        def object_hook(d):
            if "action" in d and "data" in d:
                return WsRequest(**d)
            else:
                return d
        data: WsRequest = json.loads(msg, object_hook=object_hook)
        """
        **d 是 Python 的解包語法，它將字典 d 的鍵值對解包為關鍵字參數。
        例如，如果 d 是 {'action': 'bet', 'data': {'amount': 100}}，
        那麼 WsRequest(**d) 等同於 WsRequest(action='bet', data={'amount': 100})。
        """

        action = data.action
        if action == "bet":
            # check is verify
            if not self.clients[self]["is_verify"]:
                self.write_message("你想幹嘛？？？")
                return
            self.write_message("成功下注")
        elif action == "get_game":
            self.write_message(gameManager.message_for_client())
        elif action == "login":
            username = data.data.get("username")
            token = data.data.get("token")
            login_info = User.LoginInfo(username, token)
            user = login_info.get_user()
            if user is not None:
                self.clients[self]["is_verify"] = True
                self.write_message("登入成功")
            else:
                self.write_message("登入失敗")
    


    @classmethod
    def send_updates(cls, status):
        # send status update to all connected clients
        for client in cls.clients:
            client.write_message(status)

async def status_updater():
    count = 0
    while True:
        await asyncio.sleep(1)  # update status every second
        count += 1
        GameWebSocketHandler.send_updates(
            f"Current status update count: {count}")


async def handleGame():
    while True:
        await asyncio.sleep(1)
        if gameManager.stop_bet_time < datetime.datetime.now():
            # create next game
            gameManager.create_next_game()
        # print("Current game: ", gameManager.current_game)
        # print("Stop bet time: ", gameManager.stop_bet_time)
        # print("Current time: ", datetime.datetime.now())
        # print("Time left: ", gameManager.stop_bet_time - datetime.datetime.now())


def make_app():
    return tornado.web.Application([
        (r"/status", GameWebSocketHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    # start status updater task in the event loop
    asyncio.get_event_loop().create_task(handleGame())
    tornado.ioloop.IOLoop.current().start()
