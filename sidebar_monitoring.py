import streamlit as st
import pandas as pd

def monitoring():
    with st.sidebar.expander("📊 Monitoring", expanded=False):
        st.subheader("Real-time Logs")
        log_placeholder = st.empty() # Placeholder to update logs later
        st.subheader("Trade History")
        if st.session_state['trade_history']:
            st.dataframe(pd.DataFrame(st.session_state['trade_history']))
        else:
            st.info("No trades executed yet.")