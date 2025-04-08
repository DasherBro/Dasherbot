import streamlit as st
import pytz

def advanced_config():
    with st.sidebar.expander("⚙️ Advanced", expanded=False):
        st.subheader("Timezone")
        available_timezones = pytz.all_timezones
        selected_timezone = st.selectbox("Select Timezone", available_timezones, index=available_timezones.index(st.session_state['selected_timezone']))
        if selected_timezone != st.session_state['selected_timezone']:
            st.session_state['selected_timezone'] = selected_timezone
            st.rerun()
        st.subheader("API Connection")
        api_status = "Connected" if 'exchange' in st.session_state and st.session_state['exchange'] else "Not Connected"
        st.info(f"API Status: {api_status}")
        st.subheader("Polling Interval")
        polling_interval = st.number_input("Interval (seconds)", min_value=1, value=st.session_state['polling_interval'], step=1, help="How often the bot checks for new data/signals.")
        if polling_interval != st.session_state['polling_interval']:
            st.session_state['polling_interval'] = int(polling_interval)
            st.info(f"Polling interval set to {st.session_state['polling_interval']} seconds.")
        st.subheader("Slippage Simulation (Backtest)")
        slippage = st.number_input("Slippage (%)", min_value=0.0, step=0.01, value=0.0, help="Simulated slippage percentage for backtesting.")
        st.subheader("Transaction Fees (Backtest)")
        fees = st.number_input("Transaction Fee (%)", min_value=0.0, step=0.001, value=0.0, help="Transaction fee percentage for backtesting.")