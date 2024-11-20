import yfinance as yf
import sqlite3
import pandas as pd
from datetime import datetime, timedelta 
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import pandas_datareader as web
import requests
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib import rcParams


def date(close):
    conn=sqlite3.connect("check_data.db")
    with conn:
        cursor= conn.cursor()
        sql= '''SELECT DISTINCT Close FROM NewTable where Date =?'''

        cursor.execute(sql,(close,))
        date = [items[0] for items in cursor.fetchall()]
    return date

def get_close():
    conn = sqlite3.connect('check_data.db')
    with conn:
        cursor= conn.cursor()
        sql = '''SELECT DISTINCT Close From NewTable'''
        cursor.execute(sql)
        close = [items[0] for items in cursor.fetchall()]
    return close






def download_data():
    print("download_data function is called")
    symbol = '2330.TW'
    start = '2020-01-01'
    end = (dt.datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    conn = sqlite3.connect('check_data.db')
    # 下載資料
    try:
        data = yf.download(symbol, start=start, end=end)
        cursor = conn.cursor()
        # 檢查資料表是否已經存在日期資料
        for index, row in data.iterrows():
            date_str = index.strftime('%Y-%m-%d')
            
            # 檢查該日期是否已存在於資料庫中
            cursor.execute("SELECT 1 FROM NewTable WHERE Date = ? AND Tickers = ?", (date_str, symbol))
            result = cursor.fetchone()
            
            if result is None:  # 如果該日期不存在，則插入資料
                open_price = row['Open'].iloc[0] if pd.notnull(row['Open'].iloc[0]) else None
                high = row['High'].iloc[0] if pd.notnull(row['High'].iloc[0]) else None
                low = row['Low'].iloc[0] if pd.notnull(row['Low'].iloc[0]) else None
                adj_close = row['Adj Close'].iloc[0] if pd.notnull(row['Adj Close'].iloc[0]) else None
                volume = row['Volume'].iloc[0] if pd.notnull(row['Volume'].iloc[0]) else None
                close = row['Close'].iloc[0] if pd.notnull(row['Close'].iloc[0]) else None

                
                # 插入資料
                insertSQL = """
                    INSERT OR IGNORE INTO NewTable (Date, "Open", High, Low, "Adj Close", Volume, "Close", Tickers)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(insertSQL, (date_str, open_price, high, low, adj_close, volume, close, symbol))
        conn.commit()
        messagebox.showinfo('下載狀態','下載完成')
    except Exception as e:
        print(f'Error occurred: {e}')
    finally:
        # 確保連接被關閉
        if conn:
            # 提交更改並關閉連接
            cursor.close()
            conn.close()



#calculate

def linear_regression():
    
    # 連接到 SQLite 資料庫
    conn = sqlite3.connect('check_data.db')

    # 從資料庫讀取資料
    sql = '''SELECT * FROM NewTable'''
    data_from_db = pd.read_sql(sql, conn)

    # 關閉資料庫連接
    conn.close()
    
    # 將索引轉換為日期格式
    data_from_db['Date'] = pd.to_datetime(data_from_db['Date'])
    # 將日期轉換為從最早日期起的天數
    data_from_db['Days'] = (data_from_db['Date'] - data_from_db['Date'].min()).dt.days

    X = data_from_db[['Days']]  # 自變量
    y = data_from_db['Close']  # 目標變量

    # 線性回歸模型

    '''
    LinearRegression

    SGDRegressor
    model = SGDRegressor()
    model.fit(X, y.values.ravel())



    fit_intercept: 預設為True，表示有將y軸的截距加入 ，並自動計算出最佳的截距值 ，如果為False，迴歸模型線會直接通過原點
    normalize : 是否將數據做歸一化（Normalize），預設為False
    copy_X : 預設為True，表示X會被Copied，如果為False，X會被覆蓋掉
    n_jobs : 計算模型所使使用的CPU數量，預設為1，如果傳入-1，就會使用全部的CPU


    '''
 
  

    # scaler = StandardScaler()
    # X_scarled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.4, random_state = 0)
    model = LinearRegression(fit_intercept=True,copy_X=True,n_jobs=1)
    model.fit(X_train, y_train)
    model_score = model.score(X_train, y_train)
    b = model.intercept_
    a = model.coef_
   

    
    print(f'Model Score (R²): {model_score:.4f}\nCoeficient: {a} \nIntercept: {b}')
    print("=========================================")
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test,y_pred)
    r2 = r2_score(y_test,y_pred)
    print(f'Model Score (R²): {r2:.4f}\nMean Squared Error: {mse}')
    print("=========================================")
    # if not X_test.empty:
    #     try:
    #         test_dates = data_from_db.loc[X_test.index, :].index
    #         print(test_dates[:5])
    #     except Exception as e:
    #         print(f"Error calculating test_dates: {e}")
    # else:
    #     print("X_test is empty, cannot calculate test_dates.")





    # 確保 X_test 是帶有列名稱的 DataFrame
    X_test = pd.DataFrame(X_test, columns=['Days'])
    # 提取測試集對應的日期
    test_dates = data_from_db.loc[X_test.index,'Date']
    
    y_test_pred = model.predict(X_test)
    

    # 繪圖
    plt.figure(figsize=(12, 6))
    plt.plot(data_from_db['Date'], data_from_db['Close'], label='Historical Close Price', color='Blue')

    # 使用 model 預測的值
    # 繪製測試集預測結果
    plt.plot(test_dates, y_test_pred, label='Linear Regression', color='orange')

    # 進行預測
    # 未來30天
    future_days = 30

    # 獲取最後一個日期的天數
    last_day = data_from_db['Date'].max()
    # 使用模型進行預測
    # 建立 future_x 為帶列名稱的 DataFrame
    future_x = pd.DataFrame(
    np.arange(data_from_db['Days'].max() + 1, data_from_db['Days'].max() + future_days + 1),
    columns=['Days'])
    #future_x = np.arange(data_from_db['Days'].max() + 1, data_from_db['Days'].max() + future_days + 1).reshape(-1, 1)
    predicted_price = model.predict(future_x)

    # 將預測結果轉換為日期格式，從最後一天開始
    future_dates = [last_day + pd.Timedelta(days=i) for i in range(1, future_days + 1)]

    # 顯示預測價格
    plt.plot(future_dates, predicted_price, label='Future Prediction', color='red', linestyle='--')

    # 設定
    # plt.xlim(pd.Timestamp('2020-01-01'), future_dates[-1])
    # plt.xlabel('Date')
    # plt.ylabel('Close Price')

    # #plt.ylim(min(data['Close'].iloc[0].min(),predicted_price.min())-10,max(data['Close'].iloc[0].max(),predicted_price.max())+10)
    # plt.ylim(0,1500)
    # plt.title('Close Price and Linear Regression Line with Prediction')

    # plt.legend()
    # plt.show()

    plt.xlim(data_from_db['Date'].min(), future_dates[-1])
    plt.ylim(data_from_db['Close'].min() - 10, data_from_db['Close'].max() + 10)
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title('Close Price and Linear Regression Line with Prediction')
    plt.legend()
    plt.show()


def rsi():
    # 連接到 SQLite 資料庫
    conn = sqlite3.connect('check_data.db')

    # 從資料庫讀取資料
    sql = '''SELECT * FROM NewTable'''
    data_from_db = pd.read_sql(sql, conn)

    # 關閉資料庫連接
    conn.close()

    data_from_db['Date'] = pd.to_datetime(data_from_db['Date'])
    # 將日期轉換為從最早日期起的天數
    data_from_db['Days'] = (data_from_db['Date'] - data_from_db['Date'].min()).dt.days

    
    rcParams['font.family'] = 'Microsoft JhengHei'  # 微軟正黑體（或替換為系統中的其他中文字體）
    # Step 2: 計算 RSI
    window = 14  # RSI 計算窗口

    # 計算每日價格變化
    delta = data_from_db['Close'].diff()

    # 分別計算上漲和下跌數據
    gain = delta.where(delta > 0, 0)  # 上漲數據
    loss = -delta.where(delta < 0, 0)  # 下跌數據

    # 計算平均上漲與平均下跌
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    # 計算 RS 和 RSI
    rs = avg_gain / avg_loss
    data_from_db['RSI'] = 100 - (100 / (1 + rs))

    # Step 3: 繪製圖形
    fig, axes = plt.subplots(2, 1, figsize=(8, 4))

    # 設定背景顏色為灰色
    axes[0].set_facecolor('lightgrey')
    axes[1].set_facecolor('lightgrey')

    # 繪製收盤價
    axes[0].plot(data_from_db['Days'],data_from_db['Close'], label='Close Price', color='blue')
    axes[0].set_title('台積電收盤價', fontsize=14)
    axes[0].set_xlabel('日期', fontsize=10)  # X 軸標籤
    axes[0].set_ylabel('價格 (TWD)', fontsize=10)  # Y 軸標籤
    axes[0].legend()

    # 設置 X 軸的範圍和標籤
    axes[0].set_xlim(data_from_db['Days'].min(), data_from_db['Days'].max())
    axes[0].set_xticks(data_from_db['Days'][::180])  # 每隔 30 天顯示一個標籤
    axes[0].set_xticklabels(data_from_db['Date'][::180].dt.strftime('%Y-%m-%d'))  # 日期格式化
    axes[0].legend()

    # 繪製 RSI
    axes[1].plot(data_from_db['Days'],data_from_db['RSI'], label='RSI', color='purple')
    axes[1].axhline(70, color='red', linestyle='--',
                    linewidth=0.5, label='超買區 (70)')  # 超買區
    axes[1].axhline(30, color='green', linestyle='--',
                    linewidth=0.5, label='超賣區 (30)')  # 超賣區
    axes[1].set_title('RSI 指標', fontsize=10)
    axes[1].set_xlabel('日期', fontsize=10)  # X 軸標籤
    axes[1].set_ylabel('RSI 值', fontsize=10)  # Y 軸標籤
    axes[1].legend()

    # 設置 X 軸的範圍和標籤
    axes[1].set_xlim(data_from_db['Days'].min(), data_from_db['Days'].max())
    axes[1].set_xticks(data_from_db['Days'][::180])  # 每隔 30 天顯示一個標籤
    axes[1].set_xticklabels(data_from_db['Date'][::180].dt.strftime('%Y-%m-%d'))  # 日期格式化
    axes[1].legend()



    # 調整佈局避免重疊
    plt.tight_layout()

    # 顯示圖形
    plt.show()




