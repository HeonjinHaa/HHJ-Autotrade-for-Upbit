import time
import pyupbit
import datetime
import numpy as np

access = "1vlYNWRQVZxdlmb95ALVru6rbXXjQDdjxx1nwB6n"
secret = "IJjZlUKxAAPHxkJlIxQUxzWfzWTNiiIpiy1ixWSb"

def get_ror(ticker, k, day):
    """최근 day일간 k값으로 매매했을때 해당 ticker 수익률"""
    df = pyupbit.get_ohlcv(ticker, count=day)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'],
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror

def get_best_k(ticker):
    """최근 2일 데이터로 오늘 최적 k값 결정"""
    best_k=0.01

    for k in np.arange(0.02, 1.0, 0.01):
        if get_ror(ticker, best_k, 2) < get_ror(ticker, k, 2):
            best_k = k
        

    return best_k


def get_target_price(ticker):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    k = get_best_k(ticker)

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

def get_current_price(coin):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=coin)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("Autotrade Start!")

# 자동매매 시작
while True:
    try:
        """관심목록 리스트"""
        coin_list = ["KRW-SOL", "KRW-ATOM", "KRW-DOT", "KRW-ADA", "KRW-ETH"]

        for ticker in coin_list:
            now = datetime.datetime.now()
            start_time = get_start_time(ticker)
            end_time = start_time + datetime.timedelta(days=1)

            if start_time < now < end_time - datetime.timedelta(seconds=10):
                target_price = get_target_price(ticker)
                current_price = get_current_price(ticker)
                if target_price < current_price:
                    krw = get_balance("KRW")/len(coin_list)
                    if krw > 5000:
                        upbit.buy_market_order(ticker, krw*0.9995)
            else:
                coin = get_balance(ticker) 
                if current_price*coin > 5000:
                    upbit.sell_market_order(ticker, coin*0.9995)
            time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)
