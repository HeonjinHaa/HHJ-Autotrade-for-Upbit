import time
import pyupbit
import datetime

access = "1vlYNWRQVZxdlmb95ALVru6rbXXjQDdjxx1nwB6n"
secret = "IJjZlUKxAAPHxkJlIxQUxzWfzWTNiiIpiy1ixWSb"

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

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-SOL")
        end_time = start_time + datetime.timedelta(days=1)

        coin_list = ["KRW-SOL", "KRW-ATOM", "KRW-DOT", "KRW-ADA", "KRW-ETH"]

        if start_time < now < end_time - datetime.timedelta(seconds=10):

            target_price = get_target_price("KRW-SOL", 0.3)
            current_price = get_current_price("KRW-SOL")
            if target_price < current_price:
                krw = get_balance("KRW")/len(coin_list)
                if krw > 5000:
                    upbit.buy_market_order("KRW-SOL", krw*0.9995)
            
            target_price = get_target_price("KRW-ATOM", 0.3)
            current_price = get_current_price("KRW-ATOM")
            if target_price < current_price:
                krw = get_balance("KRW")/len(coin_list)
                if krw > 5000:
                    upbit.buy_market_order("KRW-ATOM", krw*0.9995)
            
            target_price = get_target_price("KRW-DOT", 0.3)
            current_price = get_current_price("KRW-DOT")
            if target_price < current_price:
                krw = get_balance("KRW")/len(coin_list)
                if krw > 5000:
                    upbit.buy_market_order("KRW-DOT", krw*0.9995)

            target_price = get_target_price("KRW-ADA", 0.3)
            current_price = get_current_price("KRW-ADA")
            if target_price < current_price:
                krw = get_balance("KRW")/len(coin_list)
                if krw > 5000:
                    upbit.buy_market_order("KRW-ADA", krw*0.9995)

            target_price = get_target_price("KRW-ETH", 0.3)
            current_price = get_current_price("KRW-ETH")
            if target_price < current_price:
                krw = get_balance("KRW")/len(coin_list)
                if krw > 5000:
                    upbit.buy_market_order("KRW-ETH", krw*0.9995)

        else:
            coin = get_balance("SOL")
            if (coin * get_current_price("KRW-SOL")) > 5000:
                upbit.sell_market_order("KRW-SOL", coin*0.9995)
            
            coin = get_balance("ATOM")
            if (coin * get_current_price("KRW-ATOM")) > 5000:
                upbit.sell_market_order("KRW-ATOM", coin*0.9995)
            
            coin = get_balance("DOT")
            if (coin * get_current_price("KRW-DOT")) > 5000:
                upbit.sell_market_order("KRW-DOT", coin*0.9995)
            
            coin = get_balance("ADA")
            if (coin * get_current_price("KRW-ADA")) > 5000:
                upbit.sell_market_order("KRW-ADA", coin*0.9995)

            coin = get_balance("ETH")
            if (coin * get_current_price("KRW-ETH")) > 5000:
                upbit.sell_market_order("KRW-ETH", coin*0.9995)
        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)
