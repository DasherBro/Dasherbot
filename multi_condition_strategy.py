import streamlit as st

def backtesting_sidebar():
    st.sidebar.header("⚙️ Backtesting Settings")

    symbol = st.sidebar.text_input("Trading Pair", "BTC/USDT")
    timeframe = st.sidebar.selectbox("Timeframe", ["15m", "1h", "4h", "1d"], index=0)
    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")
    initial_capital = st.sidebar.number_input("Initial Capital", value=1000)

    strategy_options = ["SMA Crossover", "RSI Strategy", "MACD Crossover", "Bollinger Bands", "Breakout", "Multi-Condition Strategy"]  # Add your new strategy name
    selected_strategy = st.sidebar.selectbox("Strategy", strategy_options, index=len(strategy_options) - 1) # Default to the new strategy

    strategy_params = {}
    if selected_strategy == "SMA Crossover":
        strategy_params['short_period'] = st.sidebar.slider("Short SMA Period", 5, 50, 20)
        strategy_params['long_period'] = st.sidebar.slider("Long SMA Period", 20, 200, 100)
    elif selected_strategy == "RSI Strategy":
        strategy_params['rsi_period'] = st.sidebar.slider("RSI Period", 5, 21, 14)
        strategy_params['oversold'] = st.sidebar.slider("Oversold Level", 10, 40, 30)
        strategy_params['overbought'] = st.sidebar.slider("Overbought Level", 60, 90, 70)
    elif selected_strategy == "MACD Crossover":
        strategy_params['fast_period'] = st.sidebar.slider("Fast EMA Period", 5, 30, 12)
        strategy_params['slow_period'] = st.sidebar.slider("Slow EMA Period", 20, 60, 26)
        strategy_params['signal_period'] = st.sidebar.slider("Signal SMA Period", 5, 20, 9)
    elif selected_strategy == "Bollinger Bands":
        strategy_params['bb_period'] = st.sidebar.slider("BB Period", 10, 50, 20)
        strategy_params['bb_std'] = st.sidebar.slider("BB Std Dev", 1, 3, 2)
    elif selected_strategy == "Breakout":
        strategy_params['lookback_period'] = st.sidebar.slider("Lookback Period", 10, 100, 20)
    elif selected_strategy == "Multi-Condition Strategy":
        st.sidebar.info("This strategy uses a fixed set of 38 conditions defined in 'multi_condition_strategy.py'. No parameters to configure here.")

    backtest_button = st.sidebar.button("Run Backtest")

    return symbol, timeframe, start_date, end_date, initial_capital, selected_strategy, strategy_params, backtest_button