import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import datetime as dt
import pandas_datareader as web
import requests
import yfinance as yf
from sklearn.linear_model import LinearRegression


# 讀取歷史數據
start = dt.datetime(2022, 1, 1)
end = dt.datetime(2024, 11, 1)
data = yf.download('2330.TW', start=start, end=end)

# 將索引轉換為日期格式
data['Date'] = pd.to_datetime(data.index)
# 將日期轉換為從最早日期起的天數
data['Days'] = (data['Date'] - data['Date'].min()).dt.days

X = data[['Days']]  # 自變量
y = data['Close']  # 目標變量

# 線性回歸模型
model = LinearRegression()
model.fit(X, y)

# 繪圖
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['Close'], label='Historical Close Price', color='Blue')

# 使用 model 預測的值
plt.plot(data['Date'], model.predict(X), label='Linear Regression', color='orange')

# 進行預測
# 未來30天
future_days = 30

# 獲取最後一個日期的天數
last_day = data['Date'].max()
# 使用模型進行預測
future_x = np.arange(data['Days'].max() + 1, data['Days'].max() + future_days + 1).reshape(-1, 1)
predicted_price = model.predict(future_x)

# 將預測結果轉換為日期格式，從最後一天開始
future_dates = [last_day + pd.Timedelta(days=i) for i in range(1, future_days + 1)]

# 顯示預測價格
plt.plot(future_dates, predicted_price, label='Future Prediction', color='red', linestyle='--')

# 設定
plt.xlim(pd.Timestamp('2022-01-01'), future_dates[-1])
plt.xlabel('Date')
plt.ylabel('Close Price')

plt.title('Close Price and Linear Regression Line with Prediction')

plt.legend()
plt.show()
