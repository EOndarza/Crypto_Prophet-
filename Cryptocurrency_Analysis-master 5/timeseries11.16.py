import altair as alt
import pandas as pd
import streamlit as st
import os
import requests
from streamlit_lottie import st_lottie

alt.themes.enable("streamlit")

alt.themes.enable("streamlit")

st.set_page_config(page_title="3Coin", page_icon=":tada:", layout="wide")


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_code = load_lottieurl(
    "https://assets10.lottiefiles.com/packages/lf20_8wuout7s.json"
)


# Header
with st.container():
    st.subheader("Hi :wave:, we are insert_name.")
    st.write(
        "Our goal is to use our key indicators to track, analyze and predict how Bitcoin, Ethereum and Cardano coin prices will trend."
    )

st_lottie(lottie_code, height=300, key="crypto")

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

# st.write("## Code")

# st.write(
#     "See more in our public [GitHub"
#     " repository](https://github.com/streamlit/example-app-time-series-annotation)"
# )

# st.code(
# f"""
