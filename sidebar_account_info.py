import streamlit as st
import pandas as pd

def account_info():
    with st.sidebar.expander("💰 Account Info", expanded=False):
        st.metric("Account Balance", f"${st.session_state['account_balance']:.2f}")
        if st.session_state['open_positions']:
            st.subheader("Open Positions")
            st.dataframe(pd.DataFrame(st.session_state['open_positions']))
        else:
            st.info("No open positions.")
        st.metric("Total P&L", f"${st.session_state['pl']:.2f}")