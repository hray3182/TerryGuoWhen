import Messages
print(Messages.INTRODUCTION)

def main():
    initialbalance = 5000
    balance = initialbalance

    print("歡迎下注！")
    print("您的初始餘額為:", initialbalance)

    while True:
        print("\n您的目前餘額為:", balance)
        bet = input("請輸入您要下注的數量(按e退出):")
        
        if bet.lower() == 'e':
            print("期待您再次遊玩！")
            break

        try:
            bet = int(bet)
            if bet*100 <= 0:
                print("下注數量必須大於 0。")
                continue
            if bet*100 > balance:
                print("下注數量不能超過您的餘額。")
                continue

            balance -= bet*100
            print("您下了", bet,"注" "，剩餘餘額為:", balance)

        except ValueError:
            print("請輸入一個有效的數字或按e退出。")

if __name__ == "__main__":
    main()
