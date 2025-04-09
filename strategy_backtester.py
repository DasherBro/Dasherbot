import streamlit as st
import pandas as pd
import ccxt  # Make sure ccxt is imported if you use it for data fetching
from datetime import datetime
from strategy_backtester.strategies import sma_crossover, rsi_strategy, macd_crossover, bollinger_bands_strategy, breakout_strategy
import multi_condition_strategy  # Import your new strategy file

def run_backtest(symbol, timeframe, start_date, end_date, initial_capital, selected_strategy, strategy_params):
    exchange = st.session_state.get('exchange')
    if not exchange:
        st.error("Please connect to an exchange in the 'API Config' tab first.")
        return None

    start_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
    end_str = end_date.strftime("%Y-%m-%d %H:%M:%S")

    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=exchange.parse8601(start_str), until=exchange.parse8601(end_str), limit=1000) # Adjust limit as needed
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
    except ccxt.ExchangeError as e:
        st.error(f"Error fetching data: {e}")
        return None

    if df.empty:
        st.warning("No data fetched for the specified period.")
        return None

    st.subheader(f"Backtesting: {selected_strategy} on {symbol} ({timeframe})")
    st.write(f"Period: {start_date} to {end_date}, Initial Capital: {initial_capital}")

    if selected_strategy == "SMA Crossover":
        results_df, final_capital = sma_crossover.backtest(df.copy(), strategy_params['short_period'], strategy_params['long_period'], initial_capital)
    elif selected_strategy == "RSI Strategy":
        results_df, final_capital = rsi_strategy.backtest(df.copy(), strategy_params['rsi_period'], strategy_params['oversold'], strategy_params['overbought'], initial_capital)
    elif selected_strategy == "MACD Crossover":
        results_df, final_capital = macd_crossover.backtest(df.copy(), strategy_params['fast_period'], strategy_params['slow_period'], strategy_params['signal_period'], initial_capital)
    elif selected_strategy == "Bollinger Bands":
        results_df, final_capital = bollinger_bands_strategy.backtest(df.copy(), strategy_params['bb_period'], strategy_params['bb_std'], initial_capital)
    elif selected_strategy == "Breakout":
        results_df, final_capital = breakout_strategy.backtest(df.copy(), strategy_params['lookback_period'], initial_capital)
    elif selected_strategy == "Multi-Condition Strategy":
        # Assuming your backtest_strategy function in multi_condition_strategy.py takes the full df
        results_df, final_capital = multi_condition_strategy.backtest_strategy(df.copy(), initial_capital)
    else:
        st.error(f"Strategy '{selected_strategy}' not implemented in backtesting.")
        return None

    if results_df is not None:
        st.subheader("Backtesting Results")
        st.dataframe(results_df)
        st.write(f"Final Capital: {final_capital:.2f}")
        if initial_capital != 0:
            profit_percentage = ((final_capital - initial_capital) / initial_capital) * 100
            st.write(f"Total Profit/Loss: {final_capital - initial_capital:.2f} ({profit_percentage:.2f}%)")

    return results_df