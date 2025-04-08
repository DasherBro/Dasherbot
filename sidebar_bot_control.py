import streamlit as st

def bot_control():
    with st.sidebar.expander("⚙️ Bot Control", expanded=True):
        st.subheader("General")
        st.info(f"Current Pair: {st.session_state['selected_symbol']}")
        st.info(f"Current Timeframe: {st.session_state['selected_timeframe']}")
        st.info(f"Last Signal: {st.session_state['last_signal']}")

        if st.button("Start Bot"):
            st.session_state['bot_running'] = True
            st.success("Bot started!")
            # Add your bot starting logic here (e.g., initialize trading loop)

        if st.button("Stop Bot"):
            st.session_state['bot_running'] = False
            st.warning("Bot stopped.")
            # Add your bot stopping logic here (e.g., terminate trading loop)

        dry_run = st.checkbox("Enable Dry Run (No Real Orders)", value=True)
        if st.checkbox("Enable Trading (Requires Password)"):
            password = st.text_input("Trading Password:", type="password")
            if password == '123':  # Replace with your actual password check
                st.session_state['trading_enabled'] = True
                st.success("Trading Enabled!")
            elif password:
                st.error("Incorrect Password!")
        else:
            st.session_state['trading_enabled'] = False
        st.subheader(f"Bot Status: {'Running' if st.session_state['bot_running'] else 'Stopped'}")
        st.subheader(f"Trading Enabled: {'Yes' if st.session_state['trading_enabled'] else 'No'}")
        st.subheader(f"Dry Run: {'Yes' if dry_run else 'No'}")