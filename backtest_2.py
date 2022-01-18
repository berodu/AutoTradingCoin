import pyupbit
import matplotlib.pyplot as plt
import time
import pandas as pd

def short_trading_for_1percent(ticker):
    dfs = []
    # df = pyupbit.get_ohlcv(ticker, interval="minute3", to="20220118 09:00:00")
    df = pyupbit.get_ohlcv(ticker, interval="minute3", to="20220118 09:00:00")
    dfs.append(df)

    # 데이터 갯수 : 200 * N
    for i in range(10):
        # df = pyupbit.get_ohlcv(ticker, interval="minute3", to=df.index[0])
        df = pyupbit.get_ohlcv(ticker, interval="minute3", to=df.index[0])        
        dfs.append(df)
        time.sleep(0.2)
        
    df = pd.concat(dfs)
    df = df.sort_index()
    # print(df)

    # df['close'].plot()
    # plt.show()

    # (1) 매수 일자 판별
    cond = df['high'] >= df['open'] * 1.01
    # print(df.index[cond])

    acc_ror = 1
    sell_time = None

    # (2) 매도 조건 탐색 및 수익률 계산
    for buy_time in df.index[cond]:
        if sell_time != None and buy_time <= sell_time:
            continue
            
        target = df.loc[ buy_time : ]
        
        cond = target['high'] >= target['open'] * 1.02
        sell_candidate = target.index[cond]
        
        if len(sell_candidate) == 0:
            buy_price = df.loc[buy_time, 'open'] * 1.01
            sell_price = df.iloc[-1, 3] # 구간 종가에 매도
            acc_ror *= (sell_price / buy_price)
            break
        else:
            sell_time = sell_candidate[0]
            acc_ror *= 1.01 - 0.005
            # 수수료 0.001 + 슬리피지 0.004
    origin_ror = df.iloc[-1]['close'] / df.iloc[0]['open']
    print("origin", ticker, origin_ror)        
    return acc_ror

for ticker in ["KRW-BTC", "KRW-SAND", "KRW-DOGE", "KRW-XRP", "KRW-NEAR"]:
    ror = short_trading_for_1percent(ticker)
    print(ticker, ror)