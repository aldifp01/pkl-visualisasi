import pandas as pd
import streamlit as st
import matplotlib as plt
import altair as alt
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from st_aggrid import AgGrid
from collections import Counter
from st_aggrid import AgGrid
from itertools import chain
import re

class Toc:

    def __init__(self):
        self._items = []
        self._placeholder = None
    
    def title(self, text):
        self._markdown(text, "h1")

    def header(self, text):
        self._markdown(text, "h2", " " * 2)

    def subheader(self, text):
        self._markdown(text, "h3", " " * 4)

    def placeholder(self, sidebar=False):
        self._placeholder = st.sidebar.empty() if sidebar else st.empty()

    def generate(self):
        if self._placeholder:
            self._placeholder.markdown("\n".join(self._items), unsafe_allow_html=True)
    
    def _markdown(self, text, level, space=""):
        key = "".join(filter(str.isalnum, text)).lower()

        st.markdown(f"<{level} id='{key}'>{text}</{level}>", unsafe_allow_html=True)
        self._items.append(f"{space}* <a href='#{key}'>{text}</a>")

def bar_accuracy(acc):
    # preprocessing dataframe agar dapat diplot dengan altair
    algorithm_list = ['KMeans', 'Gaussian Mixture', 'Fuzzy CMeans']
    acc.rename(columns={acc.columns[0]: "Class"}, inplace = True)
    acc_res = pd.DataFrame()
    for algorithm in algorithm_list:
        acc_temp = acc.copy(deep=True)[["Class", algorithm]].rename(columns={algorithm:"Accuracy"})
        acc_temp.insert(2, 'Algorithm', algorithm)
        acc_res = pd.concat([acc_res, acc_temp], ignore_index=True)
    # st.write(acc_res)

    # plotting
    bar_acc = alt.Chart(acc_res).mark_bar().encode(
        x=alt.X("Algorithm", sort=acc_res['Algorithm'].unique()),
        y='Accuracy', column=alt.Column('Class', sort=acc_res['Class'].unique()),
        color='Algorithm', tooltip=['Class','Algorithm','Accuracy']
        ).properties(width=130).interactive()
    st.altair_chart(bar_acc)

def bar_silhouette(acc):
    # preprocessing dataframe agar dapat diplot dengan altair
    algorithm_list = ['KMeans', 'Gaussian Mixture', 'Fuzzy CMeans']
    acc.rename(columns={acc.columns[0]: "Class"}, inplace = True)
    acc_res = pd.DataFrame()
    for algorithm in algorithm_list:
        acc_temp = acc.copy(deep=True)[["Class", algorithm]].rename(columns={algorithm:"Silhouette Score"})
        acc_temp.insert(2, 'Algorithm', algorithm)
        acc_res = pd.concat([acc_res, acc_temp], ignore_index=True)
    # st.write(acc_res)

    # plotting
    bar_acc = alt.Chart(acc_res).mark_bar().encode(
        x=alt.X("Algorithm", sort=acc_res['Algorithm'].unique()),
        y='Silhouette Score', column=alt.Column('Class', sort=acc_res['Class'].unique()),
        color='Algorithm', tooltip=['Class','Algorithm','Silhouette Score']
        ).properties(width=130).interactive()
    st.altair_chart(bar_acc)
    # return 1

# Fungsi menampilkan clustering dataset
def view_cluster_data(Pretest,Posttest,Delta):
    with st.expander("View Encoded Dataset"):
        st.markdown("##### PreTest")
        AgGrid(Pretest)
        st.markdown("##### PostTest")
        AgGrid(Posttest)
        st.markdown("##### Delta")
        AgGrid(Delta)

# def counter_cluster(data):
#     return 1

def preposess_name(df):
    bruh = df.iloc[:,:-2].astype(str).apply(lambda x : x+' '+x.name)
    bruh["Nilai"] = df.iloc[:,-2]
    bruh["Cluster"] = df["Cluster"]
    return bruh

# def hitung_common(df,name):
#     # st.write("#### Top 2 Most Common Pattern of:",name)
#     st.write('#### Pola Emosi',name)
     
#     convert_1 = preposess_name(df)
#     df_all = pd.DataFrame()
#     for clus in range(len(convert_1["Cluster"].unique())):
#         convert = convert_1.iloc[:,:-1].loc[convert_1["Cluster"] == clus].itertuples(index=False,name=None)
#         bruh = Counter(convert).most_common(2)
#         df_new = pd.DataFrame(bruh,columns=['Pola Emosi','Jumlah'])
#         df_new['Cluster'] = clus
#         df_all = pd.concat([df_all,df_new])

#     hide_table_row_index = """
#             <style>
#             thead tr th:first-child {display:none}
#             tbody th {display:none}
#             </style>
#             """
#     st.markdown(hide_table_row_index, unsafe_allow_html=True)
#     with st.expander('View Top Pattern'):
#         st.table(df_all)
#         # st.table(df_all)
#     # return st.table(df_all)

# def hitung_jumlah_per_cluster(df):
#     df.value_counts()
#     return 1

def hitung_common(df,name):
    st.write('#### Faktor Afektif',name)
    
    convert_1 = preposess_name(df)
    df_all = pd.DataFrame()
    for clus in range(len(convert_1["Cluster"].unique())):
        convert = convert_1.iloc[:,:-1].loc[convert_1["Cluster"] == clus].itertuples(index=False,name=None)
        bruh = Counter(convert).most_common(2)
        df_new = pd.DataFrame(bruh,columns=['Faktor Afektif','Jumlah'])
        df_new['Cluster'] = clus
        df_all = pd.concat([df_all,df_new])

    hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    with st.expander('View Top Pattern'):
        st.table(df_all)
        broo = df["Cluster"].value_counts(ascending=False).rename_axis("Cluster").reset_index(name="Jumlah Anggota Per Cluster")
        st.table(broo)
    # return st.table(df_all)

def clustering():
    with pd.ExcelFile('clustering/hasil_clustering.xlsx') as xls:
        # Accuracy
        aeq_acc = pd.read_excel(xls,'aeq_acc')
        dass_acc = pd.read_excel(xls,'dass_acc')
        erq_acc = pd.read_excel(xls,'erq_acc')
        # Silhouette
        aeq_sil = pd.read_excel(xls,'aeq_sil')
        dass_sil = pd.read_excel(xls,'dass_sil')
        erq_sil = pd.read_excel(xls,'erq_sil')

        # KMeans AEQ
        aeq_kmeans_pretest = pd.read_excel(xls,'kmeans-aeq-pretest')
        aeq_kmeans_posttest = pd.read_excel(xls,'kmeans-aeq-posttest')
        aeq_kmeans_delta = pd.read_excel(xls,'kmeans-aeq-delta')
        # KMeans DASS
        dass_kmeans_pretest = pd.read_excel(xls,'kmeans-dass-pretest')
        dass_kmeans_posttest = pd.read_excel(xls,'kmeans-dass-posttest')
        dass_kmeans_delta = pd.read_excel(xls,'kmeans-dass-delta')
        # KMeans ERQ
        erq_kmeans_pretest = pd.read_excel(xls,'kmeans-erq-pretest')
        erq_kmeans_posttest = pd.read_excel(xls,'kmeans-erq-posttest')
        erq_kmeans_delta = pd.read_excel(xls,'kmeans-erq-delta')
        # KMeans ALL
        ade_kmeans_pretest = pd.read_excel(xls,'kmeans-ade-pretest')
        ade_kmeans_posttest = pd.read_excel(xls,'kmeans-ade-posttest')
        ade_kmeans_delta = pd.read_excel(xls,'kmeans-ade-delta')

        # Gaussian Mixture AEQ
        aeq_gaussian_pretest = pd.read_excel(xls,'gaussian-aeq-pretest')
        aeq_gaussian_posttest = pd.read_excel(xls,'gaussian-aeq-posttest')
        aeq_gaussian_delta = pd.read_excel(xls,'gaussian-aeq-delta')
        # Gaussian Mixture DASS
        dass_gaussian_pretest = pd.read_excel(xls,'gaussian-dass-pretest')
        dass_gaussian_posttest = pd.read_excel(xls,'gaussian-dass-posttest')
        dass_gaussian_delta = pd.read_excel(xls,'gaussian-dass-delta')
        # Gaussian Mixture ERQ
        erq_gaussian_pretest = pd.read_excel(xls,'gaussian-erq-pretest')
        erq_gaussian_posttest = pd.read_excel(xls,'gaussian-erq-posttest')
        erq_gaussian_delta = pd.read_excel(xls,'gaussian-erq-delta')
        # Gaussian Mixture ALL
        ade_gaussian_pretest = pd.read_excel(xls,'gaussian-ade-pretest')
        ade_gaussian_posttest = pd.read_excel(xls,'gaussian-ade-posttest')
        ade_gaussian_delta = pd.read_excel(xls,'gaussian-ade-delta')

        # Fuzzy CMeans AEQ
        aeq_fuzzy_pretest = pd.read_excel(xls,'fuzzy-aeq-pretest')
        aeq_fuzzy_posttest = pd.read_excel(xls,'fuzzy-aeq-posttest')
        aeq_fuzzy_delta = pd.read_excel(xls,'fuzzy-aeq-delta')
        # Fuzzy CMeans DASS
        dass_fuzzy_pretest = pd.read_excel(xls,'fuzzy-dass-pretest')
        dass_fuzzy_posttest = pd.read_excel(xls,'fuzzy-dass-posttest')
        dass_fuzzy_delta = pd.read_excel(xls,'fuzzy-dass-delta')
        # Fuzzy CMeans ERQ
        erq_fuzzy_pretest = pd.read_excel(xls,'fuzzy-erq-pretest')
        erq_fuzzy_posttest = pd.read_excel(xls,'fuzzy-erq-posttest')
        erq_fuzzy_delta = pd.read_excel(xls,'fuzzy-erq-delta')
        # Fuzzy CMeans ALL
        ade_fuzzy_pretest = pd.read_excel(xls,'fuzzy-ade-pretest')
        ade_fuzzy_posttest = pd.read_excel(xls,'fuzzy-ade-posttest')
        ade_fuzzy_delta = pd.read_excel(xls,'fuzzy-ade-delta')

        # KModes CMeans AEQ
        aeq_kmodes_pretest = pd.read_excel(xls,'kmodes-aeq-pretest')
        aeq_kmodes_posttest = pd.read_excel(xls,'kmodes-aeq-posttest')
        aeq_kmodes_delta = pd.read_excel(xls,'kmodes-aeq-delta')
        # KModes CMeans DASS
        dass_kmodes_pretest = pd.read_excel(xls,'kmodes-dass-pretest')
        dass_kmodes_posttest = pd.read_excel(xls,'kmodes-dass-posttest')
        dass_kmodes_delta = pd.read_excel(xls,'kmodes-dass-delta')
        # KModes CMeans ERQ
        erq_kmodes_pretest = pd.read_excel(xls,'kmodes-erq-pretest')
        erq_kmodes_posttest = pd.read_excel(xls,'kmodes-erq-posttest')
        erq_kmodes_delta = pd.read_excel(xls,'kmodes-erq-delta')
        # KModes CMeans ALL
        ade_kmodes_pretest = pd.read_excel(xls,'kmodes-ade-pretest')
        ade_kmodes_posttest = pd.read_excel(xls,'kmodes-ade-posttest')
        ade_kmodes_delta = pd.read_excel(xls,'kmodes-ade-delta')

    ################################################################################################################

    ################################################################################################################
    ################################################# BAGIAN HALAMAN ###############################################

    # st.title("Clustering")
    st.markdown("<h1 style='text-align: center; color: system;'>---Clustering---</h1>", unsafe_allow_html=True)
    st.sidebar.markdown("# Clustering")
    st.sidebar.markdown("## 195150207111039")
    st.sidebar.markdown("## Hasyir Daffa Ibrahim")

    st.markdown("## 1. Algortima KMeans")
    st.markdown("### 1.1. AEQ")
    # # view_cluster_data(aeq_kmeans_pretest,aeq_kmeans_posttest,aeq_kmeans_delta)
    hitung_common(aeq_kmeans_pretest.iloc[:,1:],"AEQ pada Pretest")
    hitung_common(aeq_kmeans_posttest.iloc[:,1:],"AEQ pada Posttest")
    hitung_common(aeq_kmeans_delta.iloc[:,1:],"AEQ pada Delta")
    st.markdown("<h3 style='text-align: center; color: system;'>Faktor AEQ yang mempengaruhi hasil ujian</h3>", unsafe_allow_html=True)
    st.markdown("**POSTTEST | Cluster 0 : 46 | Cluster 1 : 88 | Cluster 2 : 68**")
    st.markdown("**Cluster 0**: Moderate Class Positive, Low Class Negative, Moderate Test Positive, Low Test Negative, High PostTest")
    st.markdown("**Cluster 1**: High Class Positive, Low Class Negative, High Test Positive, Low Test Negative, High PostTest")
    st.markdown("**Cluster 2**: High Class Positive, Moderate Class Negative, High Test Positive, Moderate Test Negative, High PostTest")

    st.markdown("### 1.2. DASS")
    # view_cluster_data(dass_kmeans_pretest,dass_kmeans_posttest,dass_kmeans_delta)
    hitung_common(dass_kmeans_pretest.iloc[:,1:],"DASS pada Pretest")
    hitung_common(dass_kmeans_posttest.iloc[:,1:],"DASS pada Posttest")
    hitung_common(dass_kmeans_delta.iloc[:,1:],"DASS pada Delta")
    st.markdown("<h3 style='text-align: center; color: system;'>Faktor DASS yang mempengaruhi hasil ujian</h3>", unsafe_allow_html=True)
    st.markdown("**POSTTEST | Cluster 0 : 80 | Cluster 1 : 57 | Cluster 2 : 65**")
    st.markdown("**Cluster 0**: Normal Depression, Normal Anxiety, Normal Stress, High PostTest")
    st.markdown("**Cluster 1**: Normal Depression, Normal Anxiety, Normal Stress, Moderate PostTest")
    st.markdown("**Cluster 2**: Normal Depression, Moderate Anxiety, Normal Stress, High PostTest")

    st.markdown("### 1.3. ERQ")
    # view_cluster_data(erq_kmeans_pretest,erq_kmeans_posttest,erq_kmeans_delta)
    hitung_common(erq_kmeans_pretest.iloc[:,1:],"ERQ pada Pretest")
    hitung_common(erq_kmeans_posttest.iloc[:,1:],"ERQ pada Posttest")
    hitung_common(erq_kmeans_delta.iloc[:,1:],"ERQ pada Delta")
    st.markdown("<h3 style='text-align: center; color: system;'>Faktor ERQ yang mempengaruhi hasil ujian</h3>", unsafe_allow_html=True)
    st.markdown("**POSTTEST | Cluster 0 : 76 | Cluster 1 : 67 | Cluster 2 : 59**")
    st.markdown("**Cluster 0**: Moderate CRF, Moderate ESF, High PostTest")
    st.markdown("**Cluster 1**: High CRF, Moderate ESF, High PostTest")
    st.markdown("**Cluster 2**: Moderate CRF, Moderate ESF, Moderate PostTest")

    st.markdown("### 1.4. AEQ + DASS + ERQ")
    # st.markdown("#### All Emotions Towards Test with KMeans")
    # view_cluster_data(ade_kmeans_pretest,ade_kmeans_posttest,ade_kmeans_delta)
    hitung_common(ade_kmeans_pretest.iloc[:,1:],"menggunakan KMeans pada Pretest")
    hitung_common(ade_kmeans_posttest.iloc[:,1:],"menggunakan KMeans pada Posttest")
    hitung_common(ade_kmeans_delta.iloc[:,1:],"menggunakan KMeans pada Delta")

    #Penjelaasan KMEANS keseluruhan 
    st.markdown("<h3 style='text-align: center; color: system;'>Ringkasan KMeans</h3>", unsafe_allow_html=True)
    st.markdown("**PRETEST | Cluster 0 : 68 | Cluster 1 : 85 | Cluster 2 : 49**")
    st.markdown("**Cluster 0**: Moderate Class Positive , Moderate Class Negative , Moderate Test Positive , Moderate Test Negative , Normal Depression , Mild Anxiety , Normal Stress , Moderate CRF , Moderate ESF , High PreTest")
    st.markdown("**Cluster 1**: High Class Positive , Low Class Negative , High Test Positive , Low Test Negative , Normal Depression , Normal Anxiety , Normal Stress , Moderate CRF , Moderate ESF , High PreTest")
    st.markdown("**Cluster 2**: High Class Positive , Low Class Negative , High Test Positive , Low Test Negative , Normal Depression , Normal Anxiety , Normal Stress , Moderate CRF , Moderate ESF , Moderate PreTest")
    st.markdown("**POSTTEST | Cluster 0 : 68 | Cluster 1 : 85 | Cluster 2 : 49**")
    st.markdown("**Cluster 0**: Moderate Class Positive , Moderate Class Negative , Moderate Test Positive , Moderate Test Negative , Mild Depression , Moderate Anxiety , Normal Stress , Moderate CRF , Moderate ESF , High PostTest")
    st.markdown("**Cluster 1**: High Class Positive , Low Class Negative , High Test Positive , Low Test Negative , Normal Depression , Normal Anxiety , Normal Stress , Moderate CRF , Moderate ESF , High PostTest")
    st.markdown("**Cluster 2**: Moderate Class Positive , Low Class Negative , Moderate Test Positive , Low Test Negative , Normal Depression , Mild Anxiety , Normal Stress , Moderate CRF , Moderate ESF , High PostTest")
    st.markdown("**DELTA | Cluster 0 : 52 | Cluster 1 : 69 | Cluster 2 : 81**")
    st.markdown("**Cluster 0**: High Class Positive, Low Class Negative, High Test Positive, Low Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, Positive Delta")
    st.markdown("**Cluster 1**: Moderate Class Positive, Moderate Class Negative, Moderate Test Positive, Moderate Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, Positive Delta")
    st.markdown("**Cluster 2**: Moderate Class Positive, Moderate Class Negative, Moderate Test Positive, Moderate Test Negative, Mild Depression, Moderate Anxiety, Normal Stress, Moderate CRF, Moderate ESF, Positive Delta")
    st.markdown("<hr></hr><hr></hr>", unsafe_allow_html=True)

    
    st.markdown("## 2. Algortima Gaussian Mixture")
    st.markdown("### 2.1. AEQ")
    # view_cluster_data(aeq_gaussian_pretest,aeq_gaussian_posttest,aeq_gaussian_delta)
    hitung_common(aeq_gaussian_pretest.iloc[:,1:],"AEQ pada Pretest")
    hitung_common(aeq_gaussian_posttest.iloc[:,1:],"AEQ-Gaussia pada osttest")
    hitung_common(aeq_gaussian_delta.iloc[:,1:],"AEQ pada Delta")
    st.markdown("<h3 style='text-align: center; color: system;'>Faktor AEQ yang mempengaruhi hasil ujian</h3>", unsafe_allow_html=True)
    st.markdown("**POSTTEST | Cluster 0 : 46 | Cluster 1 : 88 | Cluster 2 : 68**")
    st.markdown("**Cluster 0**: Moderate Class Positive, Moderate Class Negative, Moderate Test Positive, Moderate Test Negative, High PostTest")
    st.markdown("**Cluster 1**: High Class Positive, Low Class Negative, High Test Positive, Low Test Negative, High PostTest")
    st.markdown("**Cluster 2**: High Class Positive, Moderate Class Negative, High Test Positive, Moderate Test Negative, High PostTest")

    st.markdown("### 2.2. DASS")
    # view_cluster_data(dass_gaussian_pretest,dass_gaussian_posttest,dass_gaussian_delta)
    hitung_common(dass_gaussian_pretest.iloc[:,1:],"DASS pada Pretest")
    hitung_common(dass_gaussian_posttest.iloc[:,1:],"DASS pada Posttest")
    hitung_common(dass_gaussian_delta.iloc[:,1:],"DASS pada Delta")
    st.markdown("<h3 style='text-align: center; color: system;'>Faktor DASS yang mempengaruhi hasil ujian</h3>", unsafe_allow_html=True)
    st.markdown("**POSTTEST | Cluster 0 : 36 | Cluster 1 : 106 | Cluster 2 : 58**")
    st.markdown("**Cluster 0**: Mild Depression, Moderate Anxiety, Normal Stress, High PostTest")
    st.markdown("**Cluster 1**: Normal Depression, Normal Anxiety, Normal Stress, High PostTest")
    st.markdown("**Cluster 2**: Normal Depression, Normal Anxiety, Normal Stress, Moderate PostTest")

    st.markdown("### 2.3. ERQ")
    # view_cluster_data(erq_gaussian_pretest,erq_gaussian_posttest,erq_gaussian_delta)
    hitung_common(erq_gaussian_pretest.iloc[:,1:],"ERQ pada Pretest")
    hitung_common(erq_gaussian_posttest.iloc[:,1:],"ERQ pada Posttest")
    hitung_common(erq_gaussian_delta.iloc[:,1:],"ERQ pada Delta")
    st.markdown("<h3 style='text-align: center; color: system;'>Faktor ERQ yang mempengaruhi hasil ujian</h3>", unsafe_allow_html=True)
    st.markdown("**POSTTEST | Cluster 0 : 40 | Cluster 1 : 108 | Cluster 2 : 54**")
    st.markdown("**Cluster 0**: Moderate CRF, Moderate ESF, Moderate PostTest")
    st.markdown("**Cluster 1**: Moderate CRF, Moderate ESF, High PostTest")
    st.markdown("**Cluster 2**: High CRF, Moderate ESF, High PostTest")

    st.markdown("### 2.4. AEQ + DASS + ERQ")
    # view_cluster_data(ade_gaussian_pretest,ade_gaussian_posttest,ade_gaussian_delta)
    # st.markdown("#### All Emotions Towards Test with Gaussian Mixture")
    hitung_common(ade_gaussian_pretest.iloc[:,1:],"menggunakan Gaussian Mixture pada Pretest")
    hitung_common(ade_gaussian_posttest.iloc[:,1:],"menggunakan Gaussian Mixture pada Posttest")
    hitung_common(ade_gaussian_delta.iloc[:,1:],"menggunakan Gaussian Mixture pada Delta")
    # st.markdown("#### Ringkasan")
    #Penjelaasan Gaussian keseluruhan 
    st.markdown("<h3 style='text-align: center; color: system;'>Ringkasan Gaussian Mixture</h3>", unsafe_allow_html=True)
    st.markdown("**PRETEST | Cluster 0 : 62 | Cluster 1 : 89 | Cluster 2 : 51**")
    st.markdown("**Cluster 0**: Moderate Class Positive, Moderate Class Negative, Moderate Test Positive, Moderate Test Negative, Normal Depression, Mild Anxiety, Normal Stress, Moderate CRF, Moderate ESF, High PreTest")
    st.markdown("**Cluster 1**: High Class Positive, Low Class Negative, High Test Positive, Low Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, High PreTest")
    st.markdown("**Cluster 2**: High Class Positive, Low Class Negative, High Test Positive, Low Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, Moderate PreTest")
    st.markdown("**POSTTEST | Cluster 0 : 55 | Cluster 1 : 89 | Cluster 2 : 58**")
    st.markdown("**Cluster 0**: High Class Positive, Low Class Negative, High Test Positive, Low Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, Moderate PostTest")
    st.markdown("**Cluster 1**: High Class Positive, Low Class Negative, High Test Positive, Low Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, High PostTest")
    st.markdown("**Cluster 2**: Moderate Class Positive, Moderate Class Negative, Moderate Test Positive, Moderate Test Negative, Mild Depression, Moderate Anxiety, Normal Stress, Moderate CRF, Moderate ESF, High PostTest")
    st.markdown("**DELTA | Cluster 0 : 49 | Cluster 1 : 81 | Cluster 2 : 72**")
    st.markdown("**Cluster 0**: High Class Positive, Low Class Negative, High Test Positive, Low Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, Negative Delta")
    st.markdown("**Cluster 1**: High Class Positive, Low Class Negative, High Test Positive, Low Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, Positive Delta")
    st.markdown("**Cluster 2**: Moderate Class Positive, Moderate Class Negative, Moderate Test Positive, Moderate Test Negative, Mild Depression, Moderate Anxiety, Normal Stress, Moderate CRF, Moderate ESF, Positive Delta")
    st.markdown("<hr></hr><hr></hr>", unsafe_allow_html=True)
   
    st.markdown("## 3. Algortima Fuzzy CMeans")
    st.markdown("### 3.1. AEQ")
    # view_cluster_data(aeq_fuzzy_pretest,aeq_fuzzy_posttest,aeq_fuzzy_delta)
    hitung_common(aeq_fuzzy_pretest.iloc[:,1:],"AEQ pada Pretest")
    hitung_common(aeq_fuzzy_posttest.iloc[:,1:],"AEQ pada Posttest")
    hitung_common(aeq_fuzzy_delta.iloc[:,1:],"AEQ pada Delta")
    st.markdown("<h3 style='text-align: center; color: system;'>Faktor AEQ yang mempengaruhi hasil ujian</h3>", unsafe_allow_html=True)
    st.markdown("**POSTTEST | Cluster 0 : 65 | Cluster 1 : 63 | Cluster 2 : 74**")
    st.markdown("**Cluster 0**: Moderate Class Positive, Low Class Negative, Moderate Test Positive, Low Test Negative, High PostTest")
    st.markdown("**Cluster 1**: Moderate Class Positive, Moderate Class Negative, Moderate Test Positive, Moderate Test Negative, High PostTest")
    st.markdown("**Cluster 2**: High Class Positive, Low Class Negative, High Test Positive, Low Test Negative, High PostTest")

    st.markdown("### 3.2. DASS")
    # view_cluster_data(dass_fuzzy_pretest,dass_fuzzy_posttest,dass_fuzzy_delta)
    hitung_common(dass_fuzzy_pretest.iloc[:,1:],"DASS pada Pretest")
    hitung_common(dass_fuzzy_posttest.iloc[:,1:],"DASS pada Posttest")
    hitung_common(dass_fuzzy_delta.iloc[:,1:],"DASS pada Delta")
    st.markdown("<h3 style='text-align: center; color: system;'>Faktor DASS yang mempengaruhi hasil ujian</h3>", unsafe_allow_html=True)
    st.markdown("**POSTTEST | Cluster 0 : 76 | Cluster 1 : 57 | Cluster 2 : 69**")
    st.markdown("**Cluster 0**: Normal Depression, Normal Anxiety, Normal Stress, High PostTest")
    st.markdown("**Cluster 1**: Normal Depression, Normal Anxiety, Normal Stress, Moderate PostTest")
    st.markdown("**Cluster 2**: Normal Depression, Moderate Anxiety, Normal Stress, High PostTest")

    st.markdown("### 3.3. ERQ")
    # view_cluster_data(erq_fuzzy_pretest,erq_fuzzy_posttest,erq_fuzzy_delta)
    hitung_common(erq_fuzzy_pretest.iloc[:,1:],"ERQ pada Pretest")
    hitung_common(erq_fuzzy_posttest.iloc[:,1:],"ERQ pada Posttest")
    hitung_common(erq_fuzzy_delta.iloc[:,1:],"ERQ pada Delta")
    st.markdown("<h3 style='text-align: center; color: system;'>Faktor ERQ yang mempengaruhi hasil ujian</h3>", unsafe_allow_html=True)
    st.markdown("**POSTTEST | Cluster 0 : 84 | Cluster 1 : 47 | Cluster 2 : 71**")
    st.markdown("**Cluster 0**: Moderate CRF, Moderate ESF, High PostTest")
    st.markdown("**Cluster 1**: Moderate CRF, Moderate ESF, Moderate PostTest")
    st.markdown("**Cluster 2**: High CRF, Moderate ESF, High PostTest")

    st.markdown("### 3.4. AEQ + DASS + ERQ")
    # st.markdown("#### All Emotions Towards Test with Fuzzy CMeans")
    # view_cluster_data(ade_fuzzy_pretest,ade_fuzzy_posttest,ade_fuzzy_delta)
    hitung_common(ade_fuzzy_pretest.iloc[:,1:],"menggunakan Fuzzy CMeans pada Pretest")
    hitung_common(ade_fuzzy_posttest.iloc[:,1:],"menggunakan Fuzzy CMeans pada Posttest")
    hitung_common(ade_fuzzy_delta.iloc[:,1:],"menggunakan Fuzzy CMeans pada Delta")
    #Penjelaasan Fuzzy CMeans keseluruhan 
    st.markdown("<h3 style='text-align: center; color: system;'>Ringkasan Fuzzy CMeans</h3>", unsafe_allow_html=True)
    st.markdown("**PRETEST | Cluster 0 : 62 | Cluster 1 : 89 | Cluster 2 : 51**")
    st.markdown("**Cluster 0**: High Class Positive, Low Class Negative, High Test Positive, Low Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, High PreTest")
    st.markdown("**Cluster 1**: Moderate Class Positive, Moderate Class Negative, Moderate Test Positive, Moderate Test Negative, Normal Depression, Mild Anxiety, Normal Stress, Moderate CRF, Moderate ESF, High PreTest")
    st.markdown("**Cluster 2**: High Class Positive, Low Class Negative, High Test Positive, Low Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, Moderate PreTest")
    st.markdown("**POSTTEST | Cluster 0 : 55 | Cluster 1 : 89 | Cluster 2 : 58**")
    st.markdown("**Cluster 0**: Moderate Class Positive, Low Class Negative, Moderate Test Positive, Low Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, High PostTest")
    st.markdown("**Cluster 1**: Moderate Class Positive, Moderate Class Negative, Moderate Test Positive, Moderate Test Negative, Mild Depression, Moderate Anxiety, Normal Stress, Moderate CRF, Moderate ESF, High PostTest")
    st.markdown("**Cluster 2**: High Class Positive, Low Class Negative, High Test Positive, Low Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, High PostTest")
    st.markdown("**DELTA | Cluster 0 : 49 | Cluster 1 : 81 | Cluster 2 : 72**")
    st.markdown("**Cluster 0**: High Class Positive, Moderate Class Negative, High Test Positive, Low Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, Positive Delta")
    st.markdown("**Cluster 1**: Moderate Class Positive, Moderate Class Negative, Moderate Test Positive, Moderate Test Negative, Mild Depression, Moderate Anxiety, Normal Stress, Moderate CRF, Moderate ESF, Positive Delta")
    st.markdown("**Cluster 2**: High Class Positive, Low Class Negative, High Test Positive, Low Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, Positive Delta")
    st.markdown("<hr></hr><hr></hr>", unsafe_allow_html=True)
    # st.markdown("## 4. Algortima KModes")
    # st.markdown("### 4.1. AEQ")
    # # view_cluster_data(aeq_kmodes_pretest,aeq_kmodes_posttest,aeq_kmodes_delta)
    # hitung_common(aeq_kmodes_pretest.iloc[:,1:],"AEQ-KModes-Pretest")
    # hitung_common(aeq_kmodes_posttest.iloc[:,1:],"AEQ-KModes-Posttest")
    # hitung_common(aeq_kmodes_delta.iloc[:,1:],"AEQ-KModes-Delta")
    # st.markdown("### 4.2. DASS")
    # hitung_common(dass_kmodes_pretest.iloc[:,1:],"DASS-KModes-Pretest")
    # hitung_common(dass_kmodes_posttest.iloc[:,1:],"DASS-KModes-Posttest")
    # hitung_common(dass_kmodes_delta.iloc[:,1:],"DASS-KModes-Delta")
    # # view_cluster_data(dass_kmodes_pretest,dass_kmodes_posttest,dass_kmodes_delta)
    # st.markdown("### 4.3. ERQ")
    # # view_cluster_data(erq_kmodes_pretest,erq_kmodes_posttest,erq_kmodes_delta)
    # hitung_common(erq_kmodes_pretest.iloc[:,1:],"ERQ-KModes-Pretest")
    # hitung_common(erq_kmodes_posttest.iloc[:,1:],"ERQ-KModes-Posttest")
    # hitung_common(erq_kmodes_delta.iloc[:,1:],"ERQ-KModes-Delta")
    # st.markdown("### 4.4. AEQ + DASS + ERQ")
    # st.markdown("#### All Emotions Towards Test with KModes")
    # # view_cluster_data(ade_kmodes_pretest,ade_kmodes_posttest,ade_kmodes_delta)
    # hitung_common(ade_kmodes_pretest.iloc[:,1:],"ALL-KModes-Pretest")
    # hitung_common(ade_kmodes_posttest.iloc[:,1:],"ALL-KModes-Posttest")
    # hitung_common(ade_kmodes_delta.iloc[:,1:],"ALL-KModes-Delta")
    # st.markdown("#### Ringkasan")
    
    st.markdown("<hr></hr><hr></hr>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: system;'>Ringkasan Keseluruhan</h3>", unsafe_allow_html=True)
    st.markdown("Tiga cluster yang dibentuk dengan KMeans, Gaussian Mixture, Fuzzy CMeans terhadap AEQ, DASS dan ERQ digunakan untuk melakukan karakterisasi mahasiswa berdasarkan pola faktor afektif nya terhadap hasil ujian")
    st.markdown("<h4>Dalam KMeans, berikut merupakan faktor afektif yang mempengaruhi nilai ujian mahasiswa:</h4>", unsafe_allow_html=True)
    st.markdown("**Cluster 0 : 68 | Cluster 1 : 85 | Cluster 2 : 49**")
    st.markdown("**Cluster 0**: Moderate Class Positive , Moderate Class Negative , Moderate Test Positive , Moderate Test Negative , Mild Depression , Moderate Anxiety , Normal Stress , Moderate CRF , Moderate ESF , High PostTest")
    st.markdown("**Cluster 1**: High Class Positive , Low Class Negative , High Test Positive , Low Test Negative , Normal Depression , Normal Anxiety , Normal Stress , Moderate CRF , Moderate ESF , High PostTest")
    st.markdown("**Cluster 2**: Moderate Class Positive , Low Class Negative , Moderate Test Positive , Low Test Negative , Normal Depression , Mild Anxiety , Normal Stress , Moderate CRF , Moderate ESF , High PostTest")
    st.markdown("<h4>Dalam Gaussian Mixture, berikut merupakan faktor afektif yang mempengaruhi nilai ujian mahasiswa:</h4>", unsafe_allow_html=True)
    st.markdown("**Cluster 0 : 55 | Cluster 1 : 89 | Cluster 2 : 58**")
    st.markdown("**Cluster 0**: High Class Positive, Low Class Negative, High Test Positive, Low Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, Moderate PostTest")
    st.markdown("**Cluster 1**: High Class Positive, Low Class Negative, High Test Positive, Low Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, High PostTest")
    st.markdown("**Cluster 2**: Moderate Class Positive, Moderate Class Negative, Moderate Test Positive, Moderate Test Negative, Mild Depression, Moderate Anxiety, Normal Stress, Moderate CRF, Moderate ESF, High PostTest")
    st.markdown("<h4>Dalam Fuzzy CMeans, berikut merupakan faktor afektif yang mempengaruhi nilai ujian mahasiswa:</h4>", unsafe_allow_html=True)
    st.markdown("**Cluster 0 : 55 | Cluster 1 : 89 | Cluster 2 : 58**")
    st.markdown("**Cluster 0**: Moderate Class Positive, Low Class Negative, Moderate Test Positive, Low Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, High PostTest")
    st.markdown("**Cluster 1**: Moderate Class Positive, Moderate Class Negative, Moderate Test Positive, Moderate Test Negative, Mild Depression, Moderate Anxiety, Normal Stress, Moderate CRF, Moderate ESF, High PostTest")
    st.markdown("**Cluster 2**: High Class Positive, Low Class Negative, High Test Positive, Low Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, High PostTest")

    # st.markdown("**PRETEST**")
    # st.markdown("**Cluster 0**: Moderate Class Positive, Moderate Class Negative, Moderate Test Positive, Moderate Test Negative, Normal Depression, Mild Anxiety, Normal Stress, Moderate CRF, Moderate ESF, High PreTest ")
    # st.markdown("**Cluster 1**: High Class Positive, Low Class Negative, High Test Positive, Low Test_Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, High PreTest")
    # st.markdown("**Cluster 2**: High Class Positive, Low Class Negative, High Test Positive, Low Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, Moderate PreTest")
    # st.markdown("**POSTTEST**")
    # st.markdown("**Cluster 0**: Moderate Class Positive, Moderate Class Negative, Moderate Test Positive, Moderate Test Negative, Mild Depression, Moderate Anxiety, Normal Stress, Moderate CRF, Moderate ESF, High PostTest")
    # st.markdown("**Cluster 1**: High Class Positive, Low Class Negative, High Test Positive, Low Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, High PostTest")
    # st.markdown("**Culster 2**: Moderate Class Positive , Low Class Negative , Moderate Test Positive , Low Test Negative , Normal Depression , Mild Anxiety , Normal Stress , Moderate CRF , Moderate ESF , High PostTest ")
    # st.markdown("**DELTA**")
    # st.markdown("**Cluster 0**: Moderate Class Positive, Low Class Negative, Moderate Test Positive, Low Test Negative, Normal Depression, Mild Anxiety, Normal Stress, Moderate CRF, Moderate ESF, Positive Delta")
    # st.markdown("**Cluster 1**: Moderate Class Positive, Moderate Class Negative, Moderate Test Positive, Moderate Test Negative, Mild Depression, Moderate Anxiety, Normal Stress, Moderate CRF, Moderate ESF, Positive Delta")
    # st.markdown("**Cluster 2**: High Class Positive, Low Class Negative, High Test Positive, Low Test Negative, Normal Depression, Normal Anxiety, Normal Stress, Moderate CRF, Moderate ESF, Positive Delta")
    st.markdown("<hr></hr><hr></hr>", unsafe_allow_html=True)
    st.markdown("<hr></hr><hr></hr>", unsafe_allow_html=True)

    st.markdown("## 4. Evaluasi Silhouette Score")
    st.markdown("### 4.1. AEQ Silhouette Score")
    bar_silhouette(aeq_sil)
    st.markdown("### 4.2. DASS Silhouette Score")
    bar_silhouette(dass_sil)
    st.markdown("### 4.3. ERQ Silhouette Score")
    bar_silhouette(erq_sil)

    st.markdown("<hr></hr><hr></hr>", unsafe_allow_html=True)
    st.markdown("## 5. Evaluasi Accuracy Score")
    st.markdown("### 5.1. AEQ Accuracy Score")
    bar_accuracy(aeq_acc)
    st.markdown("### 5.2. DASS Accuracy Score")
    bar_accuracy(dass_acc)
    st.markdown("### 5.3. ERQ Accuracy Score")
    bar_accuracy(erq_acc)

