import pandas as pd

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