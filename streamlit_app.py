import pandas as pd
import streamlit as st
import matplotlib as plt
import altair as alt
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from st_aggrid import AgGrid

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()
brush = alt.selection_interval()  
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['x'], empty='none')

def main_page():
    st.title("INI PRAKTIK KERJA LAPANGAN")
    st.markdown("![Alt Text](https://c.tenor.com/wq2ni1rSdrMAAAAd/gemini31292.gif)")

def page2():
    ################################################################################################################
    ###########################################LIST DATAFRAME UNTUK ASOSIASI########################################
    #Dataframe untuk visualisasi
    ap_general = pd.read_csv("asosiasi/ap_general.csv")
    ap_combine = pd.read_csv("asosiasi/ap_combine.csv")
    ap_vis = pd.read_csv("asosiasi/ap_vis.csv")
    apriori_delta = pd.read_csv("asosiasi/apriori_delta.csv")
    apriori_general = pd.read_csv("asosiasi/apriori_general.csv")
    apriori_posttest = pd.read_csv("asosiasi/apriori_posttest.csv")
    apriori_pretest = pd.read_csv("asosiasi/apriori_pretest.csv")
    df_rule_fp = pd.read_csv("asosiasi/df_rule_fp.csv")
    fp_vis = pd.read_csv("asosiasi/fp_vis.csv")
    #Rule
    rule_ap_delta = pd.read_csv("asosiasi/rule_ap_delta.csv")
    rule_ap_general = pd.read_csv("asosiasi/rule_ap_general.csv")
    rule_ap_pretest = pd.read_csv("asosiasi/rule_ap_pretest.csv")
    rule_ap_posttest = pd.read_csv("asosiasi/rule_ap_posttest.csv")
    #Time
    df_time_ap_1 = pd.read_csv("asosiasi/df_time_ap_1.csv")
    df_time_ap_2 = pd.read_csv("asosiasi/df_time_ap_2.csv")
    df_time_fp = pd.read_csv("asosiasi/df_time_fp.csv")
    ################################################################################################################

    ################################################################################################################
    ################################################# BAGIAN HALAMAN ###############################################
    st.markdown("# Asosiasi")
    st.sidebar.markdown("# Asosiasi")
    st.sidebar.markdown("## 195150201111034")
    st.sidebar.markdown("## Aldi Fianda Putra")

    st.markdown("## 1. Algoritma Apriori")
    st.markdown("##### Rule yang diperoleh Secara Umum")

    #tabel secara umum atau keseluruhan
    AgGrid(rule_ap_general)

    st.markdown("##### Frekuensi consequent/RHS yang sering muncul")
    AgGrid(ap_general)
    
    #barchart general
    bar_ap_general = alt.Chart(ap_general).mark_bar().encode(
        x=alt.X('Consequents', type='nominal', sort=None),y='counts',
        ).properties(width=800,height=600).interactive()
    st.altair_chart(bar_ap_general)
    st.markdown("Visualisasi diatas menunjukan frekuensi consequent yang muncul secara umum. Terlihat 'High Postest' memiliki jumlah kemunculan paling tinggi, diikuti 'Normal Stress' dan 'Moderate ESF'.")
    

    st.markdown("#### Rule yang diperoleh untuk RHS Pre Test, Post Test dan Delta")

    st.markdown("##### Frekuensi consequent/RHS yang sering muncul")    
    #barchart pretest, posttest dan delta
    bar_ap_vis = alt.Chart(ap_vis).mark_bar().encode(
        x=alt.X('Consequents', type='nominal', sort=None),y='Jumlah',
        ).properties(width=800,height=600).interactive()
    st.altair_chart(bar_ap_vis)

    #Scatter plot
    scatter_ap_com  = alt.Chart(ap_combine).mark_point().encode(x=alt.Y('Support',scale=alt.Scale(zero=False)), y=alt.Y('Confidence',scale=alt.Scale(zero=False)),color='Lift',tooltip=['Antecedents','Consequents','Support', 'Confidence','Lift']).properties(width=800,height=600).interactive()
    st.altair_chart(scatter_ap_com)



    st.markdown("## 2. Algoritma FP-Growth")

    st.markdown("#### Rule yang diperoleh untuk RHS Pre Test, Post Test dan Delta")

    #barchart pretest, posttest dan delta
    bar_fp_vis = alt.Chart(fp_vis).mark_bar().encode(
        x=alt.X('Consequents', type='nominal', sort=None),y='Jumlah',tooltip=['Consequents', 'Jumlah']).properties(width=800,height=600).interactive()
    st.altair_chart(bar_fp_vis)

    #Scatter plot
    scatter_fp_com  = alt.Chart(df_rule_fp).mark_point().encode(x=alt.Y('Support',scale=alt.Scale(zero=False)), y=alt.Y('Confidence',scale=alt.Scale(zero=False)),color='Lift',tooltip=['Antecedents','Consequents','Support', 'Confidence','Lift']).properties(width=800,height=600).interactive()
    st.altair_chart(scatter_fp_com)





    #Line chart
    highlight = alt.selection(type='single', on='mouseover',
                          fields=['variable'], nearest=True, empty="none")


    st.markdown("## 3. Perbandingan Algoritma")
def page3():
    st.markdown("# Clustering")
    st.sidebar.markdown("# Clustering")
    st.markdown("![Alt Text](https://c.tenor.com/WB9lrgDX2m8AAAAM/samin.gif)")

def page4():
    st.markdown("# Klasifikasi")
    st.sidebar.markdown("# Klasifikasi")
    st.markdown("![Alt Text](https://c.tenor.com/gfLUuOk0fVoAAAAd/i-have-hired-kanye-to-stare-at-you-kanye-west.gif )")

page_names_to_funcs = {
    "Main Page": main_page,
    "Asosiasi": page2,
    "Clustering": page3,
    "Klasifikasi": page4,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

