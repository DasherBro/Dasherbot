import streamlit as st

def futures_trading_config():
    with st.sidebar.expander("📊 Futures Trading", expanded=True):
        st.subheader("Futures Settings")
        margin_mode = st.selectbox("Margin Mode", ["cross", "isolated"], index=["cross", "isolated"].index(st.session_state['margin_mode']), help="Choose between cross or isolated margin for futures trading.")
        if margin_mode != st.session_state['margin_mode']:
            st.session_state['margin_mode'] = margin_mode
            st.rerun()
        position_mode = st.selectbox("Position Mode", ["single", "hedge"], index=["single", "hedge"].index(st.session_state['position_mode']), help="Choose between single (one direction per symbol) or hedge (both long and short allowed).")
        if position_mode != st.session_state['position_mode']:
            st.session_state['position_mode'] = position_mode
            st.rerun()
        leverage = st.number_input("Leverage", min_value=1, max_value=125, value=st.session_state['leverage'], step=1, help="Set the leverage for futures trading. Higher leverage increases risk.")
        if leverage != st.session_state['leverage']:
            st.session_state['leverage'] = int(leverage)
            st.rerun()