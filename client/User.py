class User:
    def __init__(
        self,
        username: str,
        create_time: str,
        token: str = None,
        balance: int = 0
    ) -> None:
        self.username = username
        self.token: str = token
        self.create_time = create_time
        self.balance = balance
        
