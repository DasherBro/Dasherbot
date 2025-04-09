import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta  # Removed 'date' as it seems unused here
import pytz
import bitget_api
import signal_generation
import strategy_backtester
import trading_pairs  # Import the new module

# --- Import Sidebar Sections (now used in tabs) ---
from sidebar_bot_control import bot_control
from sidebar_api_configuration import api_configuration
from sidebar_futures_trading import futures_trading_config
from sidebar_strategy import strategy_config
from sidebar_account_info import account_info
from sidebar_monitoring import monitoring
from sidebar_backtesting import backtesting_config
from sidebar_advanced import advanced_config
from sidebar_screener import screener_config

# --- Configuration ---
default_symbol = trading_pairs.bitget_futures_pairs[0] if trading_pairs.bitget_futures_pairs else 'BTC/USDT'
available_symbols = trading_pairs.bitget_futures_pairs
default_timeframe = '1h'
available_timeframes = ['1m', '2m', '3m', '5m', '6m', '9m', '10m', '15m', '18m', '20m', '27m', '30m', '54m', '72m', '90m', '359m', '718m', '1436m', '1h', '2h', '3h', '4h', '6h', '9h', '12h', '1d', '2d', '3d', '4d', '9d', '14d', '18d']
default_timezone = 'UTC'
available_timezones = pytz.all_timezones
montreal_tz = pytz.timezone('America/Montreal')
default_short_period = 20
default_long_period = 50
now_montreal = datetime.now(montreal_tz)
default_backtest_start_date = (now_montreal - timedelta(days=7)).date()
default_backtest_start_time = now_montreal.time().replace(hour=0, minute=0, second=0, microsecond=0)
default_backtest_end_date = now_montreal.date()
default_backtest_end_time = now_montreal.time().replace(hour=23, minute=59, second=59, microsecond=0)

# --- Initialize Session State ---
if 'bot_running' not in st.session_state: st.session_state['bot_running'] = False
if 'trading_enabled' not in st.session_state: st.session_state['trading_enabled'] = False
if 'last_signal' not in st.session_state: st.session_state['last_signal'] = None
if 'selected_timeframe' not in st.session_state: st.session_state['selected_timeframe'] = default_timeframe
if 'selected_symbol' not in st.session_state: st.session_state['selected_symbol'] = default_symbol
if 'margin_mode' not in st.session_state: st.session_state['margin_mode'] = 'cross'
if 'position_mode' not in st.session_state: st.session_state['position_mode'] = 'single'
if 'leverage' not in st.session_state: st.session_state['leverage'] = 1
if 'short_period' not in st.session_state: st.session_state['short_period'] = default_short_period
if 'long_period' not in st.session_state: st.session_state['long_period'] = default_long_period
if 'backtest_start_date' not in st.session_state: st.session_state['backtest_start_date'] = default_backtest_start_date
if 'backtest_start_time' not in st.session_state: st.session_state['backtest_start_time'] = default_backtest_start_time
if 'backtest_end_date' not in st.session_state: st.session_state['backtest_end_date'] = default_backtest_end_date
if 'backtest_end_time' not in st.session_state: st.session_state['backtest_end_time'] = default_backtest_end_time
if 'take_profit_percent' not in st.session_state: st.session_state['take_profit_percent'] = 0.0
if 'stop_loss_percent' not in st.session_state: st.session_state['stop_loss_percent'] = 0.0
if 'order_quantity' not in st.session_state: st.session_state['order_quantity'] = 0.01
if 'polling_interval' not in st.session_state: st.session_state['polling_interval'] = 5
if 'trade_history' not in st.session_state: st.session_state['trade_history'] = []
if 'account_balance' not in st.session_state: st.session_state['account_balance'] = 1000.0
if 'open_positions' not in st.session_state: st.session_state['open_positions'] = []
if 'pl' not in st.session_state: st.session_state['pl'] = 0.0
if 'selected_timezone' not in st.session_state: st.session_state['selected_timezone'] = default_timezone  # Add this line

# --- Main Application with Tabs ---
st.title("Dasher - Bitget Trading Bot")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "⚙️ Bot Control",
    "🔑 API Config",
    "📊 Futures",
    "📈 Strategy",
    "💰 Account",
    "📊 Monitoring",
    "🧪 Backtest",
    "⚙️ Advanced",
    "🔎 Screener",
])

with tab1:
    bot_control()

with tab2:
    api_configuration()

with tab3:
    futures_trading_config()

with tab4:
    strategy_config()

with tab5:
    account_info()

with tab6:
    monitoring()

with tab7:
    backtesting_config()

with tab8:
    advanced_config()

with tab9:
    screener_config()

# --- Main Application Logic (plotting and bot execution) ---
def get_local_time(utc_dt, timezone_str):
    tz = pytz.timezone(timezone_str)
    return utc_dt.astimezone(tz)

if st.session_state.get('selected_symbol'):  # Access from session state
    selected_symbol = st.session_state['selected_symbol']
    selected_timeframe = st.session_state['selected_timeframe'] # Access from session state
    exchange_instance = st.session_state.get('exchange')

    if exchange_instance:
        data_df = bitget_api.fetch_ohlcv(exchange_instance, selected_symbol, selected_timeframe, limit=100)
        if not data_df.empty:
            data_df['timestamp'] = pd.to_datetime(data_df['timestamp'], unit='ms', utc=True)
            data_df['timestamp'] = data_df['timestamp'].apply(lambda dt: get_local_time(dt, st.session_state['selected_timezone']))
            data_df = signal_generation.calculate_sma(data_df, st.session_state['short_period'])
            data_df = signal_generation.calculate_sma(data_df, st.session_state['long_period'])
            data_df = signal_generation.generate_signals(data_df, st.session_state['short_period'], st.session_state['long_period'])

            # --- Plotting ---
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.7, 0.3])
            fig.add_trace(go.Candlestick(x=data_df['timestamp'], open=data_df['open'], high=data_df['high'], low=data_df['low'], close=data_df['close'], name='Candlestick'), row=1, col=1)
            fig.add_trace(go.Scatter(x=data_df['timestamp'], y=data_df[f'SMA_{st.session_state["short_period"]}'], line=dict(color='blue'), name=f'SMA {st.session_state["short_period"]}'), row=1, col=1)
            fig.add_trace(go.Scatter(x=data_df['timestamp'], y=data_df[f'SMA_{st.session_state["long_period"]}'], line=dict(color='orange'), name=f'SMA {st.session_state["long_period"]}'), row=1, col=1)
            fig.add_trace(go.Bar(x=data_df['timestamp'], y=data_df['volume'], name='Volume'), row=2, col=1)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for the selected symbol and timeframe.")
    else:
        st.warning("Please connect to an exchange in the 'API Config' tab to fetch data.")
else:
    st.info("Please select a trading pair in the 'Bot Control' tab.")

# You can keep the 'import backtesting' line as it's likely used in the backtesting_config function.