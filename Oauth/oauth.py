import streamlit as st 
import asyncio
import requests
from urllib.parse import urlencode
import string
import random
from urllib.parse import urlencode, quote

_STKEY = 'ST_OAUTH'

@st.cache_resource(ttl=300)
def qparms_cache(key):
    return {}

def logout():
    if _STKEY in st.session_state:
        del st.session_state[_STKEY]

def string_num_generator(size):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

def show_auth_link(config, label):
    state_parameter = string_num_generator(15)
    qp_dict = {
        'redirect_uri': config['redirect_uri'], 
        'client_id': config['client_id'], 
        'response_type': 'code', 
        'state': state_parameter,
        'scope': config['scope'],
    }
    
    query_params = urlencode(qp_dict)
    request_url = f"{config['authorization_endpoint']}?{query_params}"
    if st.query_params:
        qpcache = qparms_cache(state_parameter)
        qpcache = st.query_params
    google_widget_html = f"""
    <a href="{request_url}" target="_self">
        <img src="https://www.google.com.tw/favicon.ico" alt="Google Logo" width="30" height="30">
        {label}
    </a>
"""
    st.markdown(google_widget_html, unsafe_allow_html=True)
    st.stop()

def st_outh(config, label):

    if 'code' not in st.query_params.to_dict():
        show_auth_link(config, label)
    code = st.query_params['code']
    state = st.query_params['state']

    theaders = {
                        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
                    }
    tdata = {
                    'grant_type': 'authorization_code', 
                    'redirect_uri': config['redirect_uri'],
                    'client_id': config['client_id'],
                    'client_secret': config['client_secret'],
                    'scope': config['scope'],
                    'state': state,
                    'code': code,
                }
    try:
        ret = requests.post(config['token_endpoint'], headers=theaders, data=urlencode(tdata).encode("utf-8"))
        ret.raise_for_status()
        token = ret.json()
    except requests.exceptions.RequestException as e:
        st.error(e) 
        show_auth_link(config, label)

    st.session_state[_STKEY] = token
    st.markdown("This (and below) is only seen after logged in")
    if _STKEY in st.session_state:
        st.button("Logout", on_click=logout)
    return token
    