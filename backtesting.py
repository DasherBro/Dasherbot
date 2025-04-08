import pandas as pd

def run_backtest(df):
    balance = 1000  # Initial simulated balance
    position = 0
    trades = []
    buy_price = None  # Initialize buy_price

    for i in range(len(df)):
        if df['buy_signal'].iloc[i] and position == 0:
            buy_price = df['close'].iloc[i]
            position = 1
            trades.append({'timestamp': df['timestamp'].iloc[i], 'action': 'buy', 'price': buy_price})
        elif df['sell_signal'].iloc[i] and position > 0:
            sell_price = df['close'].iloc[i]
            if buy_price is not None:  # Check if buy_price has been assigned
                profit = (sell_price - buy_price)
                balance += profit
                position = 0
                trades.append({'timestamp': df['timestamp'].iloc[i], 'action': 'sell', 'price': sell_price, 'profit': profit, 'balance': balance})
                buy_price = None  # Reset buy_price after selling
            else:
                print("Warning: Sell signal encountered before a buy. Skipping trade.") # Or handle this differently
                pass # Or potentially reset position to 0 if that makes sense for your logic

    return pd.DataFrame(trades), balance