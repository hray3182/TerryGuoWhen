from User import User
from Bet import Bet
state_map = {
    0: "開放下注",
    1: "統計階段",
    2: "公告結果"
}
# 當前賽事 xxxxxxx 期 
# 當前賽事狀態：公告結果(黃色)
# 用戶名: Ray, 當前餘額: 10,000
# 目前的下注： 
# 1. 下注號碼: [1, 2, 3] 下注數量: 10
# 2. 下注號碼: [1, 3, 7] 下注數量: 5
# 3. 下注號碼: [1, 2, 5] 下注數量: 5

# 恭喜[username]中了 2,000元

class InGameMsg():
    # 賽事狀態: 0: 開放下注,  1: 統計階段, 2: 公告結果
    def __init__(self, game_id: str, game_state: int, user: User, current_bets: list[Bet], earn: int=None) -> None:
        self.game_id = game_id
        self.game_state = game_state
        self.user = user
        self.current_bets = current_bets
        self.earn = earn

    def __str__(self):
        output = f"當前賽事: {self.game_id}\n"
        output += f"當前賽事狀態：{state_map[self.game_state]}\n"
        output += f"用戶名：{self.user.username}, 當前餘額: {self.user.balance}\n"
        output += "目前的下注：\n"

        for i in range(len(self.current_bets)):
            output += f"{i + 1}. 下注號碼：{str(self.current_bets[i].nums)}, 下注數量: {self.current_bets[i].bet_amount}\n"

        if self.earn != None:
            output+= "\n"
            output += f"恭喜{self.user.username}中了 {self.earn}元"

        return output
    
 
def PrintInGameMsg(game_id: str, game_state: int, user: User, current_bets: list[Bet], earn: int=None):

        output = f"當前賽事: {game_id}\n"
        output += f"當前賽事狀態：{state_map[game_state]}\n"
        output += f"用戶名：{user.username}, 當前餘額: {user.balance}\n"
        output += "目前的下注：\n"

        for i in range(len(current_bets)):
            output += f"{i + 1}. 下注號碼：{str(current_bets[i].nums)}, 下注數量: {current_bets[i].bet_amount}\n"

        if earn != None:
            output+= "\n"
            output += f"恭喜{user.username}中了 {earn}元"

        print(output)



INTRODUCTION = chr(27) + "[2J" +"""
每一分鐘生成一場賽事,每次從 1-10 中選出 3 個數字

相同數字的數量  出現概率    倍率
    3           0.83%       50
    2           17.50%      3
    1           52.50%      1
    0           30%        -1
    
每個玩家初始金額有 5000 塊,每注 100 塊,可以自由選擇下注數,每場賽事結束之後更新排行榜。
"""

MENU = chr(27) + "[2J" + """
1. 進入遊戲
2. 遊戲說明
"""

if __name__ == "__main__":
    user = User("Ray", "2024-05-01 22:48:03.327078")
    bet1 = Bet(1, 2, 3, 10)
    bet2 = Bet(1, 3, 7, 5)
    bet3 = Bet(1, 2, 5, 5)
    current_bets = [bet1, bet2, bet3]
    earn = 2000
    PrintInGameMsg("xxxxxxx", 2, user, current_bets, 5000)



