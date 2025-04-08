import ccxt
import pandas as pd
from datetime import datetime

def fetch_ohlcv(exchange, symbol, timeframe, since=None, limit=None):
    try:
        if since:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
        else:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
        return df
    except ccxt.NetworkError as e:
        print(f"Bitget API Network Error in fetch_ohlcv: {e}")
        return pd.DataFrame()
    except ccxt.ExchangeError as e:
        print(f"Bitget API Exchange Error in fetch_ohlcv: {e}")
        return pd.DataFrame()

def calculate_sma(df, period):
    df[f'SMA_{period}'] = df['close'].rolling(window=period).mean()
    return df

def generate_signals(df, short_period, long_period):
    df['signal'] = 0
    df['short_above_long'] = df[f'SMA_{short_period}'] > df[f'SMA_{long_period}']
    df['buy_signal'] = (df['short_above_long']) & (~df['short_above_long'].shift(1).fillna(False))
    df['sell_signal'] = (~df['short_above_long']) & (df['short_above_long'].shift(1).fillna(False))
    df.loc[df['buy_signal'], 'signal'] = 1
    df.loc[df['sell_signal'], 'signal'] = -1
    return df

def run_backtest(df):
    balance = 1000  # Initial simulated balance
    position = 0
    trades = []

    for i in range(len(df)):
        if df['buy_signal'].iloc[i] and position == 0:
            buy_price = df['close'].iloc[i]
            position = 1
            trades.append({'timestamp': df['timestamp'].iloc[i], 'action': 'buy', 'price': buy_price})
        elif df['sell_signal'].iloc[i] and position > 0:
            sell_price = df['close'].iloc[i]
            profit = (sell_price - buy_price)
            balance += profit
            position = 0
            trades.append({'timestamp': df['timestamp'].iloc[i], 'action': 'sell', 'price': sell_price, 'profit': profit, 'balance': balance})

    return pd.DataFrame(trades), balance