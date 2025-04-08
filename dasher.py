import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta, date
import pytz
import bitget_api
import signal_generation
import backtesting
import trading_pairs  # Import the new module

# --- Configuration ---
default_symbol = trading_pairs.bitget_futures_pairs[0] if trading_pairs.bitget_futures_pairs else 'BTC/USDT' # Default to the first futures pair if the list isn't empty
available_symbols = trading_pairs.bitget_futures_pairs
default_timeframe = '1m'
available_timeframes = ['1m'] + [f'{i*9}m' for i in range(2, 7)] + \
                        [f'{i*9}h' for i in range(1, 6)] + \
                        [f'{i*9}d' for i in range(1, 3)] # Up to 18 days
montreal_tz = pytz.timezone('America/Montreal')
default_short_period = 20
default_long_period = 50
now_montreal = datetime.now(montreal_tz)
default_backtest_start_date = (now_montreal - timedelta(days=7)).date()
default_backtest_start_time = now_montreal.time().replace(hour=0, minute=0, second=0, microsecond=0)