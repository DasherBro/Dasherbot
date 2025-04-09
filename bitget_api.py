import ccxt

def initialize_exchange(api_key, secret, password=None):
    """
    Initializes the ccxt Bitget exchange object with API credentials.

    Args:
        api_key (str): The user's Bitget API key.
        secret (str): The user's Bitget API secret.
        password (str, optional): The user's Bitget passphrase. Defaults to None.

    Returns:
        ccxt.bitget: An initialized ccxt Bitget exchange object.
    """
    params = {
        'apiKey': api_key,
        'secret': secret,
    }
    if password:
        params['password'] = password
    exchange = ccxt.bitget(params)
    return exchange

def fetch_ohlcv(exchange, symbol, timeframe='1h', limit=100):
    """
    Fetches OHLCV (Open, High, Low, Close, Volume) data from Bitget.

    Args:
        exchange (ccxt.bitget): An initialized ccxt Bitget exchange object.
        symbol (str): The trading pair symbol (e.g., 'BTC/USDT').
        timeframe (str): The timeframe for the data (e.g., '1m', '1h', '1d').
        limit (int): The number of data points to retrieve.

    Returns:
        pandas.DataFrame: A Pandas DataFrame containing the OHLCV data with columns
                          'timestamp', 'open', 'high', 'low', 'close', 'volume'.
                          Returns an empty DataFrame if there's an error.
    """
    import pandas as pd
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except ccxt.ExchangeError as e:
        print(f"Bitget exchange error fetching {symbol} OHLCV: {e}")
        return pd.DataFrame()
    except ccxt.NetworkError as e:
        print(f"Bitget network error fetching {symbol} OHLCV: {e}")
        return pd.DataFrame()
    except ccxt.RequestTimeout as e:
        print(f"Bitget request timeout fetching {symbol} OHLCV: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"An unexpected error occurred fetching {symbol} OHLCV: {e}")
        return pd.DataFrame()

# You can add more functions here for other Bitget API interactions
# like fetching balances, placing orders, etc.