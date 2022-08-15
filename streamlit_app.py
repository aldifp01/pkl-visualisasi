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
    st.markdown("![Alt Text](https://c.tenor.com/wq2ni1rSdrMAAAAd/gemini31292.gif)")

def page2():
    st.markdown("# Asosiasi")
    st.sidebar.markdown("# Asosiasi")
    st.markdown("![Alt Text](https://c.tenor.com/3me9CyyZG8cAAAAC/friday-night.gif)")

def page3():
    st.markdown("# Clustering")
    st.sidebar.markdown("# Clustering")
    st.markdown("![Alt Text](https://c.tenor.com/WB9lrgDX2m8AAAAM/samin.gif)")

def page4():
    st.markdown("# Klasifikasi")
    st.sidebar.markdown("# Klasifikasi")
    st.markdown("![Alt Text](https://c.tenor.com/gfLUuOk0fVoAAAAd/i-have-hired-kanye-to-stare-at-you-kanye-west.gif)")

page_names_to_funcs = {
    "Main Page": main_page,
    "Page 2": page2,
    "Page 3": page3,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

