class Bet:
    def __init__(self, num1: int, num2: int, num3: int, bet_amount: int) -> None:
        self.nums = [num1, num2, num3] 
        self.bet_amount = bet_amount
        self.nums.sort()
