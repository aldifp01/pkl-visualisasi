import pandas as pd
import streamlit as st
import matplotlib as plt
import altair as alt
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from st_aggrid import AgGrid
from collections import Counter


# fungsi mencetak group bar plot
def acc_bar_plot(acc):
    # preprocessing dataframe agar dapat diplot dengan altair
    algorithm_list = ['Naive Bayes', 'Support Vector Machine', 'K-Nearest Neighbor']
    acc.rename(columns={acc.columns[0]: "Class"}, inplace = True)
    acc_res = pd.DataFrame()
    for algorithm in algorithm_list:
        acc_temp = acc.copy(deep=True)[["Class", algorithm]].iloc[:-1].rename(columns={algorithm:"Accuracy"})
        acc_temp.insert(2, 'Algorithm', algorithm)
        acc_res = pd.concat([acc_res, acc_temp], ignore_index=True)
    # st.write(acc_res)

    # plotting
    bar_acc = alt.Chart(acc_res).mark_bar().encode(
        x=alt.X("Algorithm", sort=acc_res['Algorithm'].unique()),
        y='Accuracy', column=alt.Column('Class', sort=acc_res['Class'].unique()),
        color='Algorithm', tooltip=['Class','Algorithm','Accuracy']
        ).properties(width=130)
    st.altair_chart(bar_acc)


# fungsi menampilkan confusion matrix
def view_conf_matrix(NB, SVM, KNN):
    with st.expander("Show Content"):
        st.write("Naive Bayes")
        AgGrid(NB)
        st.write("Support Vector Machine")
        AgGrid(SVM)
        st.write("K-Nearest Neighbor")
        AgGrid(KNN)


# fungsi preprocessing data ringkasan akurasi klasifikasi
def get_acc_summary(classification, acc):
    algorithm_list = ['Naive Bayes', 'Support Vector Machine', 'K-Nearest Neighbor']
    acc_res = pd.DataFrame()
    for algorithm in algorithm_list:
        acc_temp = pd.DataFrame(acc.copy(deep=True)[[algorithm]].iloc[-1]).transpose().rename(columns={algorithm:"Accuracy"})
        acc_temp.insert(0, 'Classification', classification)
        acc_temp.insert(2, 'Algorithm', algorithm)
        acc_res = pd.concat([acc_res, acc_temp], ignore_index=True)
    return acc_res


def klasifikasi():
    # Read Dataframe
    ## Classficcation Report 
    acc_aeq = pd.read_excel('klasifikasi/classification_report.xlsx', sheet_name='aeq')
    acc_dass = pd.read_excel('klasifikasi/classification_report.xlsx', sheet_name='dass')
    acc_erq = pd.read_excel('klasifikasi/classification_report.xlsx', sheet_name='erq')
    acc_ne = pd.read_excel('klasifikasi/classification_report.xlsx', sheet_name='nilai_emosi')
    acc_ce = pd.read_excel('klasifikasi/classification_report.xlsx', sheet_name='class_emosi')

    ## Confusion Matrix Report
    cm_aeq_NB = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='aeq_NB')
    cm_aeq_SVM = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='aeq_SVM')
    cm_aeq_KNN = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='aeq_KNN')

    cm_dass_NB = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='dass_NB')
    cm_dass_SVM = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='dass_SVM')
    cm_dass_KNN = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='dass_KNN')

    cm_erq_NB = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='erq_NB')
    cm_erq_SVM = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='erq_SVM')
    cm_erq_KNN = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='erq_KNN')

    cm_ne_NB = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='ne_NB')
    cm_ne_SVM = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='ne_SVM')
    cm_ne_KNN = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='ne_KNN')

    cm_ce_NB = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='ce_NB')
    cm_ce_SVM = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='ce_SVM')
    cm_ce_KNN = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='ce_KNN')


    st.markdown("# Klasifikasi")
    st.sidebar.markdown("# Klasifikasi")
    st.sidebar.markdown("## 195150200111039")
    st.sidebar.markdown("## Riski Darmawan")
    st.markdown("Pada klasifikasi, digunakan 3 algoritma machine learning yang akan dibandingkan performanya:")
    st.markdown("1. Naive Bayes\n2. Support Vector Machine\n3. K-Nearest Neighbor")


    ########### AEQ ############
    st.markdown("## 1. Achievement Emotion Questionnaire (AEQ-s)")
    st.markdown("#### Akurasi Model")

    # st.write(acc_aeq)
    acc_bar_plot(acc_aeq)
    
    st.markdown("#### Confusion Matrix")
    view_conf_matrix(cm_aeq_NB, cm_aeq_SVM, cm_aeq_KNN)


    ########### DASS ############
    st.markdown("## 2. Depression, Anxiety, and Stress Scale (DASS-21)")
    st.markdown("#### Akurasi Model")

    # st.write(acc_dass)
    acc_bar_plot(acc_dass)

    st.markdown("#### Confusion Matrix")
    view_conf_matrix(cm_dass_NB, cm_dass_SVM, cm_dass_KNN)


    ########### ERQ ############
    st.markdown("## 3. Emotion Regulation Questionnaire (ERQ)")
    st.markdown("#### Akurasi Model")

    # st.write(acc_erq)
    acc_bar_plot(acc_erq)

    st.markdown("#### Confusion Matrix")
    view_conf_matrix(cm_erq_NB, cm_erq_SVM, cm_erq_KNN)


    ########### Nilai Emosi ############
    st.markdown("## 4. Nilai (1)")
    st.markdown("Berdasarkan nilai emosi")
    st.markdown("#### Akurasi Model")

    # st.write(acc_ne)
    acc_bar_plot(acc_ne)

    st.markdown("### Confusion Matrix")
    view_conf_matrix(cm_ne_NB, cm_ne_SVM, cm_ne_KNN)


    ########### Klasifikasi Emosi ############
    st.markdown("## 5. Nilai (2)")
    st.markdown("Berdasarkan klasifikasi emosi")
    st.markdown("#### Akurasi Model")

    # st.write(acc_ce)
    acc_bar_plot(acc_ce)

    st.markdown("#### Confusion Matrix")
    view_conf_matrix(cm_ce_NB, cm_ce_SVM, cm_ce_KNN)
    
    
    ########### Ringkasan Klasifikasi ############
    st.markdown("## 6. Ringkasan Akurasi Klasifikasi")

    # preprocessing dataframe
    acc_sum = pd.DataFrame()
    acc_sum = pd.concat([acc_sum, get_acc_summary('AEQ-s', acc_aeq)], ignore_index=True)
    acc_sum = pd.concat([acc_sum, get_acc_summary('DASS-21', acc_dass)], ignore_index=True)
    acc_sum = pd.concat([acc_sum, get_acc_summary('ERQ', acc_erq)], ignore_index=True)
    acc_sum = pd.concat([acc_sum, get_acc_summary('Nilai Emosi', acc_ne)], ignore_index=True)
    acc_sum = pd.concat([acc_sum, get_acc_summary('Kelas Emosi', acc_ce)], ignore_index=True)
    # st.write(acc_sum)

    # plotting
    bar_sum = alt.Chart(acc_sum).mark_bar().encode(
        x=alt.X("Algorithm", sort=acc_sum['Algorithm'].unique()),
        y='Accuracy', column=alt.Column('Classification', sort=acc_sum['Classification'].unique()),
        color='Algorithm', tooltip=['Classification','Algorithm','Accuracy']
        ).properties(width=130)
    st.altair_chart(bar_sum)


    