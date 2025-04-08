import streamlit as st
from datetime import datetime
import pytz
import bitget_api  # Assuming you use this for fetching backtest data
import signal_generation
import backtesting
import pandas as pd

def backtesting_config():
    with st.sidebar.expander("🧪 Backtesting", expanded=False):
        st.subheader("Backtest Configuration")
        col1, col2 = st.columns(2)
        backtest_start_date = col1.date_input("Start Date", st.session_state['backtest_start_date'])
        backtest_start_time = col1.time_input("Start Time", st.session_state['backtest_start_time'])
        backtest_end_date = col2.date_input("End Date", st.session_state['backtest_end_date'])
        backtest_end_time = col2.time_input("End Time", st.session_state['backtest_end_time'])
        if st.button("Run Backtest"):
            start_datetime = datetime.combine(backtest_start_date, backtest_start_time).astimezone(pytz.utc)
            end_datetime = datetime.combine(backtest_end_date, backtest_end_time).astimezone(pytz.utc)
            if start_datetime >= end_datetime:
                st.error("Backtest start date/time must be before the end date/time.")
            else:
                backtest_data = bitget_api.fetch_ohlcv(st.session_state['exchange'], st.session_state['selected_symbol'], st.session_state['selected_timeframe'],
                                                      since=int(start_datetime.timestamp() * 1000),
                                                      limit=None)
                if not backtest_data.empty:
                    backtest_data = signal_generation.calculate_sma(backtest_data, st.session_state['short_period'])
                    backtest_data = signal_generation.calculate_sma(backtest_data, st.session_state['long_period'])
                    backtest_data = signal_generation.generate_signals(backtest_data.copy(), st.session_state['short_period'], st.session_state['long_period'])
                    trades_df, final_balance = backtesting.run_backtest(backtest_data.copy())
                    st.subheader("Backtest Results")
                    if not trades_df.empty:
                        st.dataframe(trades_df)
                        st.metric("Final Balance", f"${final_balance:.2f}")
                    else:
                        st.info("No trades were executed during the backtest period.")
                else:
                    st.info("No data fetched for the backtest period.")