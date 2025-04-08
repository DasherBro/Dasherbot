import streamlit as st
import ccxt
import bitget_api  # Assuming you have this

def api_configuration():
    with st.sidebar.expander("🔑 API Configuration", expanded=False):
        st.subheader("Exchange Settings")
        available_exchanges = ccxt.exchanges
        exchange_options = ['bitget'] + sorted([exchange for exchange in available_exchanges if exchange != 'bitget'])
        selected_exchange = st.selectbox("Exchange", exchange_options)

        api_key = st.text_input("API Key", type="password")
        secret = st.text_input("Secret", type="password")

        if selected_exchange == 'bitget':
            passphrase = st.text_input("Passphrase (for Bitget)", type="password")
            st.session_state['bitget_api_key'] = api_key
            st.session_state['bitget_secret'] = secret
            st.session_state['bitget_passphrase'] = passphrase
        else:
            st.session_state['api_key'] = api_key
            st.session_state['secret'] = secret
            if 'bitget_passphrase' in st.session_state:
                del st.session_state['bitget_passphrase']

        if st.button("Connect to Exchange"):
            try:
                if selected_exchange == 'bitget':
                    exchange_instance = bitget_api.initialize_exchange(api_key=api_key, secret=secret, password=passphrase)
                    st.session_state['exchange'] = exchange_instance
                elif selected_exchange in ccxt.exchanges:
                    exchange_class = getattr(ccxt, selected_exchange)
                    exchange_config = {
                        'apiKey': api_key,
                        'secret': secret,
                    }
                    # Some exchanges might require or allow other parameters
                    # You can add conditional logic here based on selected_exchange
                    # For example, for Binance:
                    # if selected_exchange == 'binance':
                    #     exchange_config['options'] = {'defaultType': 'future'}

                    exchange_instance = exchange_class(exchange_config)
                    st.session_state['exchange'] = exchange_instance
                    st.success(f"Successfully connected to {selected_exchange}!")
                else:
                    st.error(f"Exchange '{selected_exchange}' is not supported or the connection logic is not implemented yet.")

                if 'exchange' in st.session_state and st.session_state['exchange']:
                    st.success(f"Successfully connected to {selected_exchange}!")
                elif 'exchange' not in st.session_state:
                    st.error("Failed to connect to the exchange.")

            except Exception as e:
                st.error(f"Connection error: {e}")