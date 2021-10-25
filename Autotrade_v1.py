import time
import pyupbit
import datetime

access = "1vlYNWRQVZxdlmb95ALVru6rbXXjQDdjxx1nwB6n"
secret = "IJjZlUKxAAPHxkJlIxQUxzWfzWTNiiIpiy1ixWSb"

coin_list = ["KRW-SOL", "KRW-ATOM", "KRW-DOT", "KRW-ADA", "KRW-ETH", "KRW-BTC"]

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

def holding_ratio(ticker):
    holding_amount = get_balance(ticker[4:]) * get_current_price(ticker)
    total_amount = get_balance("KRW")

    for k in coin_list:
        total_amount = total_amount + (get_balance(k[4:]) * get_current_price(k))
    
    ratio = holding_amount / total_amount

    return ratio

def buy_coin(ticker):
    """매수"""
    target_price = get_target_price(ticker, 0.32)
    current_price = get_current_price(ticker)
    ratio = holding_ratio(ticker)

    if (ratio * len(coin_list) < 0.99999999) and (target_price < current_price):
        krw = get_balance("KRW")/len(coin_list)
        if krw > 5000 :
            upbit.buy_market_order(ticker, krw*0.9995)

def sell_coin(ticker):
    """매도"""
    if (get_balance(ticker[4:]) * get_current_price(ticker)) > 5000:
        upbit.sell_market_order(ticker, coin*0.9995)

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-SOL")
        end_time = start_time + datetime.timedelta(days=1)        

        if start_time < now < end_time - datetime.timedelta(seconds=60):
            for ticker in coin_list:
                buy_coin(ticker)          

        else:
            for ticker in coin_list:
                sell_coin(ticker)
            
        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)
