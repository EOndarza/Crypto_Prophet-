import streamlit as st
import pandas as pd
import requests

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()
photo = st.camera_input("Take a photo")

with header:
    st.title("The Crypto CryptKeeper")
    # st.image(https//static.wikia.nocookie.net/villains/images/5/5d/675249-crypt_keeper_large.png/revision/latest?cb=20160110153816)
    st.text("Take your crypto beyond the grave")

with dataset:
    st.header("NYC taxi dataset")
    st.markdown("**Test**")

with features:
    st.header("the features I created")


with model_training:
    st.header("Time to train the model")

sel_col, disp_col = st.columns(2)

max_depth = sel_col.slider(
    "How much money do you expect to lose in crypto?",
    min_value=10,
    max_value=100,
    value=20,
    step=10,
)

n_estimaters = sel_col.selectbox(
    "what coin should i buy?",
    options=["ETH", "BTC", "USDC", "Store cash in mattress"],
    index=0,
)
input_feature = sel_col.text_input("what is your feedback?", "favorite crypto")

option = st.sidebar.selectbox(
    "which dahsboard?", ("Stonks", "crypto", "twitter", "stocktwits")
)
st.header(option)

if option == "Stocks":
    st.subheader("Display Stonks data here ")

r = requests.get(
    "https://api.polygon.io/v1/open-close/AAPL/2020-10-14?adjusted=true&apiKey=d6c2u7wsPXaxwALpY3C9FeE1TfW0YSM8"
)
data = r.json()
st.write(data)
