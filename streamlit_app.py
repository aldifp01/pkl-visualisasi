import pandas as pd
import streamlit as st
import matplotlib as plt
import altair as alt
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from st_aggrid import AgGrid
import asosiasi_dash 
import klasifikasi_dash
import clustering_dash
import main_dash

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()
brush = alt.selection_interval()  
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['x'], empty='none')

def main_page():
    st.title("INI PRAKTIK KERJA LAPANGAN")
    st.markdown("![Alt Text](https://c.tenor.com/WB9lrgDX2m8AAAAM/samin.gif)")


def page3():
    st.markdown("# Clustering")
    st.sidebar.markdown("# Clustering")
    st.markdown("![Alt Text](https://c.tenor.com/WB9lrgDX2m8AAAAM/samin.gif)")

def page4():
    st.markdown("# Klasifikasi")
    st.sidebar.markdown("# Klasifikasi")
    st.markdown("![Alt Text](https://c.tenor.com/gfLUuOk0fVoAAAAd/i-have-hired-kanye-to-stare-at-you-kanye-west.gif )")

page_names_to_funcs = {
    "Main Page": main_dash.main_page,
    "Asosiasi": asosiasi_dash.asosiasi,
    "Clustering": clustering_dash.clustering,
    "Klasifikasi": klasifikasi_dash.klasifikasi,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

