import streamlit as st
import ccxt
import bitget_api  # Assuming you have this

def configure_api_secrets():
    with st.sidebar.expander("🔑 API Configuration", expanded=False):
        st.subheader("Exchange Settings")
        available_exchanges = ccxt.exchanges
        exchange_options = ['bitget'] + sorted([exch for exch in available_exchanges if exch != 'bitget'])
        selected_exchange = st.selectbox("Exchange", exchange_options)

        st.info("Please configure your API keys in the `.streamlit/secrets.toml` file.")
        st.markdown("Instructions: Create a folder `.streamlit` in the same directory as your script. Inside it, create a file named `secrets.toml` with your API keys (see Streamlit documentation).")
        st.warning("Remember that API keys on exchanges often expire (e.g., after 90 days). Please check your exchange account periodically and update the keys in `secrets.toml` if needed.")

        if st.button("Connect to Exchange"):
            api_key = None
            secret = None
            password = None  # Using 'password' as a more general term

            if selected_exchange == 'bitget':
                api_key = st.secrets.get("bitget_api_key")
                secret = st.secrets.get("bitget_secret")
                password = st.secrets.get("bitget_passphrase")  # Bitget uses 'passphrase'

                if not all([api_key, secret, password]):
                    st.error("Bitget API key, secret, and passphrase are required and not all found in `secrets.toml`.")
                    return
                try:
                    exchange_instance = bitget_api.initialize_exchange(api_key=api_key, secret=secret, password=password)
                    st.session_state['exchange'] = exchange_instance
                    st.success(f"Successfully connected to Bitget!")
                except Exception as e:
                    st.error(f"Connection error: {e}")

            elif selected_exchange == 'kucoin':
                api_key = st.secrets.get("kucoin_api_key")
                secret = st.secrets.get("kucoin_secret")
                password = st.secrets.get("kucoin_password")

                if not all([api_key, secret, password]):
                    st.error("KuCoin API key, secret, and password are required and not all found in `secrets.toml`.")
                    return
                try:
                    exchange_class = getattr(ccxt, selected_exchange)
                    exchange_instance = exchange_class({
                        'apiKey': api_key,
                        'secret': secret,
                        'password': password,
                    })
                    st.session_state['exchange'] = exchange_instance
                    st.success(f"Successfully connected to KuCoin!")
                except Exception as e:
                    st.error(f"Connection error: {e}")

            elif selected_exchange in ccxt.exchanges:
                api_key_name = f"{selected_exchange}_api_key".lower()
                secret_name = f"{selected_exchange}_secret".lower()

                api_key = st.secrets.get(api_key_name)
                secret = st.secrets.get(secret_name)

                if not all([api_key, secret]):
                    st.error(f"{selected_exchange.capitalize()} API key and secret are required and not both found in `secrets.toml` (look for keys like '{api_key_name}' and '{secret_name}').")
                    return

                try:
                    exchange_class = getattr(ccxt, selected_exchange)
                    exchange_instance = exchange_class({
                        'apiKey': api_key,
                        'secret': secret,
                    })
                    st.session_state['exchange'] = exchange_instance
                    st.success(f"Successfully connected to {selected_exchange}!")
                except Exception as e:
                    st.error(f"Connection error: {e}")

            else:
                st.error(f"Exchange '{selected_exchange}' is not supported or the connection logic is not implemented yet.")

            if 'exchange' in st.session_state and st.session_state['exchange']:
                pass  # Connection success message already shown
            elif 'exchange' not in st.session_state:
                st.error("Failed to connect to the exchange (check error messages above).")