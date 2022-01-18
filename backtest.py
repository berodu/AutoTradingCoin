
import pyupbit
import numpy as np

df = pyupbit.get_ohlcv("KRW-SAND", count=100)
df['range'] = (df['high'] - df['low']) * 0.4
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.002

# ror(수익율), np.where(조건문, 참, 거짓)
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)
# 누적곱 계산 (cpmprod) => 누적수익율
df['hpr'] = df['ror'].cumprod()

# DrawDown(낙폭) 계산 (누적 최대값과 현재 hpr 차이 / 누적 최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# MaxDrawDown
# print("MDD(%): ", df['dd'].max())

# 원래 수익률 : 실제 수익률
oror = df.iloc[-1]['close'] / df.iloc[0]['close']
print(oror, ":", df.iloc[-1]['hpr'])
df.to_excel("dd.xlsx")