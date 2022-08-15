import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()

def main_page():
    st.title("INI PRAKTIK KERJA LAPANGAN")
    st.markdown("![Alt Text](https://c.tenor.com/6aMWa1ms0WQAAAAd/gemini31292-confused.gif)")

def page2():
    st.markdown("# Asosiasi")
    st.sidebar.markdown("# Page 2 ❄️")

def page3():
    st.markdown("# Page 3 🎉")
    st.sidebar.markdown("# Page 3 🎉")

page_names_to_funcs = {
    "Main Page": main_page,
    "Page 2": page2,
    "Page 3": page3,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

