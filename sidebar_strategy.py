import streamlit as st

def strategy_config():
    with st.sidebar.expander("📈 Strategy", expanded=True):
        st.subheader("SMA Configuration")
        short_period = st.slider("Short SMA Period", min_value=5, max_value=50, value=st.session_state['short_period'], key="short_sma_slider", help="Period for the short-term Simple Moving Average.")
        long_period = st.slider("Long SMA Period", min_value=20, max_value=200, value=st.session_state['long_period'], key="long_sma_slider", help="Period for the long-term Simple Moving Average.")
        st.subheader("Order Settings")
        st.number_input("Order Quantity", min_value=0.001, step=0.001, value=st.session_state['order_quantity'], help="The quantity of the asset to trade per order.")
        st.number_input("Take Profit (%)", min_value=0.0, step=0.1, value=st.session_state['take_profit_percent'], help="Percentage above entry price to take profit (0 for no TP).")
        st.number_input("Stop Loss (%)", min_value=0.0, step=0.1, value=st.session_state['stop_loss_percent'], help="Percentage below entry price to stop loss (0 for no SL).")
        # Future: Trailing Stop settings can be added here