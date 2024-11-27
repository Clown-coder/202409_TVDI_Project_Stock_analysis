from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 設置中文字體
plt.rcParams['font.family'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False


def load_data(file_path):
    """
    載入並預處理股價數據
    """
    try:
        # 讀取CSV檔案
        df = pd.read_csv(file_path, parse_dates=['Date'])
        df.set_index('Date', inplace=True)

        # 選擇調整後收盤價
        data = df['Adj Close'].values

        return data, df
    except Exception as e:
        print(f"載入數據時出錯: {e}")
        return None, None


def create_dataset(dataset, look_back=1):
    """
    準備LSTM模型的數據集
    """
    X, Y = [], []
    for i in range(len(dataset)-look_back):
        X.append(dataset[i:(i+look_back)])
        Y.append(dataset[i+look_back])
    return np.array(X), np.array(Y)


def build_lstm_model(look_back):
    """
    建立LSTM模型
    """
    model = Sequential([
        LSTM(50, input_shape=(look_back, 1)),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model


def predict_stock_price(file_path):
    """
    預測股價主函數
    """
    # 載入數據
    data, original_df = load_data(file_path)

    if data is None:
        return

    # 數據歸一化
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data.reshape(-1, 1))

    # 準備訓練數據
    look_back = 30
    X, Y = create_dataset(scaled_data, look_back)

    # 重塑輸入數據
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    # 建立並訓練模型
    model = build_lstm_model(look_back)
    model.fit(X, Y, epochs=50, batch_size=32, verbose=0)

    # 準備預測
    last_sequence = scaled_data[-look_back:]
    last_sequence = np.reshape(last_sequence, (1, look_back, 1))

    # 進行未來30天預測
    predicted_scaled = []
    current_sequence = last_sequence
    for _ in range(30):
        next_pred = model.predict(current_sequence)[0]
        predicted_scaled.append(next_pred[0])
        current_sequence = np.roll(current_sequence, -1)
        current_sequence[0, -1, 0] = next_pred[0]

    # 反歸一化
    predicted = scaler.inverse_transform(
        np.array(predicted_scaled).reshape(-1, 1))

    # 計算預測的明日股價
    tomorrow_price = predicted[0][0]
    last_price = data[-1]

    # 繪圖
    plt.figure(figsize=(12, 6))
    plt.plot(original_df.index, data, label='實際股價', color='blue')

    # 預測日期
    forecast_dates = pd.date_range(start=original_df.index[-1], periods=31)[1:]
    plt.plot(forecast_dates,
             predicted.flatten(),
             label='預測股價', color='red', linestyle='--')

    # 標示最後一天的實際股價和明日預測股價
    plt.scatter(original_df.index[-1], last_price,
                color='green', s=100, label='最後一天收盤價', zorder=5)
    plt.scatter(forecast_dates[0], tomorrow_price,
                color='purple', s=100, label='明日預測股價', zorder=5)

    plt.title('台積電股價預測', fontsize=16)
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('股價', fontsize=12)

    # 添加文字說明
    plt.annotate(f'最後一天收盤價: {last_price:.2f}',
                 xy=(original_df.index[-1], last_price),
                 xytext=(10, 10),
                 textcoords='offset points')
    plt.annotate(f'明日預測股價: {tomorrow_price:.2f}',
                 xy=(forecast_dates[0], tomorrow_price),
                 xytext=(10, -10),
                 textcoords='offset points')

    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # 列印預測結果
    print(f"最後一天收盤價: {last_price:.2f}")
    print(f"明日預測股價: {tomorrow_price:.2f}")
    print(f"預測變動: {((tomorrow_price - last_price) / last_price * 100):.2f}%")

    return predicted


def main():
    # 請將檔案路徑替換為您的CSV檔案路徑
    file_path = 'tsmc_stock_data.csv'
    predict_stock_price(file_path)


if __name__ == "__main__":
    main()
