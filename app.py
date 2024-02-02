import streamlit as st
import requests
from Oauth.oauth import st_outh

from clarifai.modules.css import ClarifaiStreamlitCSS

st.set_page_config(layout="wide")
ClarifaiStreamlitCSS.insert_default_css(st)

config = {}

st.title("Google-Drive Oauth Example")
st.write("This example shows how to use the raw OAuth2 component to authenticate with a Google OAuth2 and list files from google drive")
st.markdown(" This (and above) is always seen")
session = st_outh(config, "Login with Google")

if session:
    headers = {
            "Authorization": f"Bearer {session['access_token']}",
            "Accept": "application/json",
        }
    response = requests.get("https://www.googleapis.com/drive/v3/files", headers=headers)
    if response.status_code == 200:
        files = response.json().get("files", [])
        names = [file["name"] for file in files]
        st.selectbox("Choose files from drive", names)
    else:
        print(f"Error: {response.status_code} - {response.text}")
