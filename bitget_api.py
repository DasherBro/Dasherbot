import ccxt
import pandas as pd
import streamlit as st

def initialize_exchange():
    exchange_id = 'bitget'
    try:
        if "bitget" in st.secrets:
            exchange = getattr(ccxt, exchange_id)({
                'apiKey': st.secrets["bitget"]["apiKey"],
                'secret': st.secrets["bitget"]["secret"],
            })
            return exchange
        else:
            st.warning("Bitget API keys not found in Streamlit secrets. Trading will be disabled.")
            return None
    except AttributeError:
        st.error(f"Exchange '{exchange_id}' not found.")
        st.stop()
        return None

def fetch_ohlcv(exchange, symbol, timeframe, since=None, limit=None):
    try:
        if exchange:
            if since:
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
            else:
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
            return df
        else:
            return pd.DataFrame()
    except ccxt.NetworkError as e:
        print(f"Bitget API Network Error in fetch_ohlcv: {e}")
        return pd.DataFrame()
    except ccxt.ExchangeError as e:
        print(f"Bitget API Exchange Error in fetch_ohlcv: {e}")
        return pd.DataFrame()