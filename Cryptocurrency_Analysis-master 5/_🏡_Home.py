import numpy as np
import pandas as pd
import requests
from pathlib import Path
import streamlit as st
from io import BytesIO, StringIO
import os
import plotly.express as px
import hvplot.pandas
import plotly.figure_factory as ff
import altair as alt
from streamlit_lottie import st_lottie


alt.themes.enable("streamlit")

st.set_page_config(page_title="3Coin", page_icon=":tada:", layout="wide")

# Header
with st.container():
    st.subheader("FTX 2.0")
    st.write("Your key 🔐 to Crypto")


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_code = load_lottieurl(
    "https://assets10.lottiefiles.com/packages/lf20_8wuout7s.json"
)


st_lottie(lottie_code, height=300, key="crypto")


# Header


# #@st.experimental_memo

folder_loc = os.getcwd() + "/Resources/"
file_names = [
    "historical_data_bitcoin",
    "historical_data_ethereum",
    "historical_data_cardano",
]


def get_data(folder_location: str, all_file_names: list) -> list:
    df_list = list()
    for each_file in all_file_names:
        full_file_location = folder_location + each_file + ".csv"
        temp_df = pd.read_csv(full_file_location, header=0)
        temp_df["symbol"] = each_file[len("historical_data_") :]
        temp_df = temp_df.rename(columns={"Date": "date", "Price (Close)": "price"})
        df_list.append(temp_df)
    return df_list


def transform_data(list_of_df: list) -> pd.DataFrame:
    temp_df = pd.DataFrame([])
    col_list = ["symbol", "date", "price"]
    for each_df in list_of_df:
        temp_df = temp_df.append(each_df[col_list])
    return temp_df


df_list = get_data(folder_location=folder_loc, all_file_names=file_names)
transformed_data = transform_data(df_list)

# Original time series chart. Omitted `get_chart` for clarity


@st.experimental_memo(ttl=60 * 60 * 24)
def get_chart(data):
    hover = alt.selection_single(
        fields=["date"], nearest=True, on="mouseover", empty="none",
    )

    lines = (
        alt.Chart(data, height=500, title="Evolution of stock prices")
        .mark_line()
        .encode(
            x=alt.X("date", title="Date"),
            y=alt.Y("price", title="Price"),
            color="symbol",
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(date)",
            y="price",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("date", title="Date"),
                alt.Tooltip("price", title="Price (USD)"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()


chart = get_chart(transformed_data)

st.title("⬇ Time series annotations")

st.write("Give more context to your time series using annotations!")

col1, col2, col3 = st.columns(3)
with col1:
    ticker = st.text_input("Choose a ticker (⬇💬👇ℹ️ ...)", value="⬇")
with col2:
    ticker_dx = st.slider(
        "Horizontal offset", min_value=-30, max_value=30, step=1, value=0
    )
with col3:
    ticker_dy = st.slider(
        "Vertical offset", min_value=-30, max_value=30, step=1, value=-10
    )

# Original time series chart. Omitted `get_chart` for clarity
df_list = get_data(folder_location=folder_loc, all_file_names=file_names)
transformed_data = transform_data(df_list)
chart = get_chart(transformed_data)

# Input annotations
ANNOTATIONS = [
    ("Mar 01, 2008", "Pretty good day for GOOG"),
    ("Dec 01, 2007", "Something's going wrong for GOOG & AAPL"),
    ("Nov 01, 2008", "Market starts again thanks to..."),
    ("Dec 01, 2009", "Small crash for GOOG after..."),
]

# Create a chart with annotations
annotations_df = pd.DataFrame(ANNOTATIONS, columns=["date", "event"])
annotations_df.date = pd.to_datetime(annotations_df.date)
annotations_df["y"] = 0
annotation_layer = (
    alt.Chart(annotations_df)
    .mark_text(size=15, text=ticker, dx=ticker_dx, dy=ticker_dy, align="center")
    .encode(x="date:T", y=alt.Y("y:Q"), tooltip=["event"],)
    .interactive()
)

# Display both charts together
st.altair_chart((chart + annotation_layer).interactive(), use_container_width=True)


# if option == "ETH":
#     st.image(
#         "https://s2.coinmarketcap.com/static/img/coins/200x200/1027.png", width=50,
#     )

#     eth_option = st.selectbox(
#         "Choose which graph to view..",
#         (
#             "ETH_100k",
#             "Price",
#             "transaction fees",
#             "AAC",
#             "marketcap_dominance",
#             "volatility",
#         ),
#     )
#     st.header(eth_option)

#     # col1, col2 = st.columns(2, gap="small")

#     # with col1:

#     if eth_option == "ETH_100k":
#         st.image(
#             "hvplot_images/ethereum_graphs/ethereum_100K.png", use_column_width=True
#         )

#     if eth_option == "Price":
#         st.image(
#             "hvplot_images/ethereum_graphs/ethereum_price.png",
#             use_column_width=True,
#         )

#     if eth_option == "transaction fees":
#         st.image(
#             "hvplot_images/ethereum_graphs/ethereum_transaction_fees.png",
#             use_column_width=True,
#         )

#     if eth_option == "aac":
#         st.image(
#             "hvplot_images/ethereum_graphs/ethereum_aac.png", use_column_width=True
#         )

#     if eth_option == "marketcap_dominance":
#         st.image(
#             "hvplot_images/ethereum_graphs/ethereum_marketcap_dominance.png",
#             use_column_width=True,
#         )

#     if eth_option == "volatility":
#         st.image(
#             "hvplot_images/ethereum_graphs/ethereum_volatility.png",
#             use_column_width=True,
#         )

# if option == "BTC":
#     st.image(
#         "data:image/png;base64,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",
#         width=50,
#     )

#     btc_option = st.selectbox(
#         "Choose which graph to view..",
#         (
#             "BTC_100k",
#             "Price",
#             "transaction fees",
#             "AAC",
#             "marketcap_dominance",
#             "volatility",
#         ),
#     )
#     st.header(btc_option)

#     # col1, col2 = st.columns(2, gap="small")

#     # with col1:

#     if btc_option == "BTC_100k":
#         st.image(
#             "hvplot_images/bitcoin_graphs/bitcoin_100K.png", use_column_width=True
#         )

#     if btc_option == "Price":
#         st.image(
#             "hvplot_images/bitcoin_graphs/bitcoin_price.png", use_column_width=True
#         )

#     if btc_option == "transaction fees":
#         st.image(
#             "hvplot_images/bitcoin_graphs/bitcoin_transaction_fees.png",
#             use_column_width=True,
#         )

#     if btc_option == "AAC":
#         st.image(
#             "hvplot_images/bitcoin_graphs/bitcoin_aac.png", use_column_width=True
#         )

#     if btc_option == "marketcap_dominance":
#         st.image(
#             "hvplot_images/bitcoin_graphs/bitcoin_marketcap_dominance.png",
#             use_column_width=True,
#         )

#     if btc_option == "volatility":
#         st.image(
#             "hvplot_images/bitcoin_graphs/bitcoin_volatility.png",
#             use_column_width=True,
#         )

# if option == "ADA":
#     st.image(
#         "data:image/png;base64,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",
#         width=83,
#     )

#     ada_option = st.selectbox(
#         "Choose which graph to view..",
#         (
#             "ADA_100k",
#             "Price",
#             "transaction fees",
#             "AAC",
#             "marketcap_dominance",
#             "volatility",
#         ),
#     )
#     st.header(ada_option)

#     # col1, col2 = st.columns(2, gap="small")

#     # with col1:

#     if ada_option == "ADA_100k":
#         st.image(
#             "hvplot_images/cardano_graphs/cardano_100K.png", use_column_width=True
#         )

#     if ada_option == "Price":
#         st.image(
#             "hvplot_images/cardano_graphs/cardano_price.png", use_column_width=True
#         )

#     if ada_option == "transaction fees":
#         st.image(
#             "hvplot_images/cardano_graphs/cardano_transaction_fees.png",
#             use_column_width=True,
#         )

#     if ada_option == "AAC":
#         st.image(
#             "hvplot_images/cardano_graphs/cardano_aac.png", use_column_width=True
#         )

#     if ada_option == "marketcap_dominance":
#         st.image(
#             "/Users/ericondarza/Downloads/Cryptocurrency_Analysis-master 2/hvplot_images/cardano_graphs/cardano_marketcap_dominance.png",
#             use_column_width=True,
#         )

#     if ada_option == "volatility":
#         st.image(
#             "hvplot_images/cardano_graphs/cardano_volatility.png",
#             use_column_width=True,
#         )

