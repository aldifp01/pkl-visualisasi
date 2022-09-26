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
        st.table(NB.fillna(' ').set_index('Classification'))
        st.write("Support Vector Machine")
        st.table(SVM.fillna(' ').set_index('Classification'))
        st.write("K-Nearest Neighbor")
        st.table(KNN.fillna(' ').set_index('Classification'))


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


# fungsi untuk menghapus postfix pada data nilai
def delete_postfix_nilai(df):
    return df['Class'].replace(['High PreTest'], 'High').replace(['Moderate PreTest'], 'Moderate').replace(['Low PreTest'], 'Low').replace(['High PostTest'], 'High').replace(['Moderate PostTest'], 'Moderate').replace(['Low PostTest'], 'Low').replace(['Positive Delta'], 'Positive').replace(['Negative Delta'], 'Negative')


def klasifikasi():
    # Read Dataframe
    ## Classficcation Report 
    acc_ne_def = pd.read_excel('klasifikasi/classification_report.xlsx', sheet_name='nilai_emosi')
    acc_ce_def = pd.read_excel('klasifikasi/classification_report.xlsx', sheet_name='class_emosi')
    acc_ne_tun = pd.read_excel('klasifikasi/classification_report.xlsx', sheet_name='nilai_emosi_htuning')
    cr_ne_tun = pd.read_excel('klasifikasi/classification_report.xlsx', sheet_name='cr_algorithm')

    ## Confusion Matrix Report
    cm_ne_def_NB = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='ne_def_NB')
    cm_ne_def_SVM = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='ne_def_SVM')
    cm_ne_def_KNN = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='ne_def_KNN')

    cm_ce_def_NB = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='ce_def_NB')
    cm_ce_def_SVM = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='ce_def_SVM')
    cm_ce_def_KNN = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='ce_def_KNN')

    cm_ne_tun_NB = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='ne_NB')
    cm_ne_tun_SVM = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='ne_SVM')
    cm_ne_tun_KNN = pd.read_excel('klasifikasi/confmatrix_report.xlsx', sheet_name='ne_KNN')


    # st.markdown("# Klasifikasi")
    st.markdown("<h1 style='text-align: center; color: system;'>---Klasifikasi---</h1>", unsafe_allow_html=True)
    st.markdown("<hr></hr><hr></hr>", unsafe_allow_html=True)
    st.sidebar.markdown("# Klasifikasi")
    st.sidebar.markdown("## 195150200111039")
    st.sidebar.markdown("## Riski Darmawan")
    st.markdown("Pada klasifikasi, digunakan 3 algoritma machine learning yang akan dibandingkan performanya:")
    st.markdown("1. Naive Bayes\n2. Support Vector Machine\n3. K-Nearest Neighbor")
    st.markdown("<hr></hr>", unsafe_allow_html=True)


    ########### Nilai Emosi ############
    st.markdown("## 1. Klasifikasi Nilai (1)")
    st.markdown("Berdasarkan nilai emosi")
    st.markdown("#### Akurasi Model")

    # st.write(acc_ne_def)
    acc_bar_plot(acc_ne_def)
    st.write('''Pada visualisasi di atas, diketahui bahwa algoritma yang dapat mengklasifikasi data Nilai Emosi dengan cukup baik hanyalah Support Vector Machine. Hal ini dapat dilihat dari akurasi yang ditunjukkan diagram batang, di mana akurasi Support Vector Machine berada mendekati 80% dan di atas 90%, sedangkan Naive Bayes dan K-Nearest Neighbor hanya di bawah 80%.''')

    st.markdown("#### Confusion Matrix")
    cm_ne_def_NB['Class'] = delete_postfix_nilai(cm_ne_def_NB)
    cm_ne_def_SVM['Class'] = delete_postfix_nilai(cm_ne_def_SVM)
    cm_ne_def_KNN['Class'] = delete_postfix_nilai(cm_ne_def_KNN)
    view_conf_matrix(cm_ne_def_NB, cm_ne_def_SVM, cm_ne_def_KNN)
    st.markdown("<hr></hr>", unsafe_allow_html=True)


    ########### Klasifikasi Emosi ############
    st.markdown("## 2. Klasifikasi Nilai (2)")
    st.markdown("Berdasarkan klasifikasi emosi")
    st.markdown("#### Akurasi Model")

    # st.write(acc_ce_def)
    acc_bar_plot(acc_ce_def)
    st.write('''Pada visualisasi di atas, diketahui bahwa ketiga algoritma dapat mengklasifikasikan data Class Emosi dengan akurasi rendah. Hal ini dapat dilihat dari akurasi yang ditunjukkan diagram batang, di mana akurasi tiap algoritma tidak ada yang mencapai 80%, bahkan hanya di sekitar 55%.''')

    st.markdown("#### Confusion Matrix")
    cm_ce_def_NB['Class'] = delete_postfix_nilai(cm_ce_def_NB)
    cm_ce_def_SVM['Class'] = delete_postfix_nilai(cm_ce_def_SVM)
    cm_ce_def_KNN['Class'] = delete_postfix_nilai(cm_ce_def_KNN)
    view_conf_matrix(cm_ce_def_NB, cm_ce_def_SVM, cm_ce_def_KNN)
    st.markdown("<hr></hr>", unsafe_allow_html=True)

    
    ########### Ringkasan Klasifikasi ############
    st.markdown("## 3. Ringkasan Akurasi Klasifikasi")

    # preprocessing dataframe
    acc_sum_def = pd.DataFrame()
    acc_sum_def = pd.concat([acc_sum_def, get_acc_summary('Nilai Emosi', acc_ne_def)], ignore_index=True)
    acc_sum_def = pd.concat([acc_sum_def, get_acc_summary('Kelas Emosi', acc_ce_def)], ignore_index=True)
    # st.write(acc_sum)

    # plotting
    bar_sum_def = alt.Chart(acc_sum_def).mark_bar().encode(
        x=alt.X("Algorithm", sort=acc_sum_def['Algorithm'].unique()),
        y='Accuracy', column=alt.Column('Classification', sort=acc_sum_def['Classification'].unique()),
        color='Algorithm', tooltip=['Classification','Algorithm','Accuracy']
        ).properties(width=130)
    st.altair_chart(bar_sum_def)

    st.write('''Pada ringkasan visualisasi di atas, didapatkan bahwa hasil akurasi pada klasifikasi Class Emosi lebih rendah jika dibandingkan dengan klasifikasi nilai menggunakan data Nilai Emosi. Hal ini sangat dimungkinkan terjadi karena klasifikasi Class Emosi menggunakan data regulasi emosi secara langsung atau dengan kata lain generalisasi / kesimpulan dari emosi yang dimiliki mahasiswa. Sedangkan klasifikasi Nilai Emosi menggunakan data yang membentuk regulasi emosi mahasiswa sehingga data menjadi lebih banyak dan spesifik. Oleh sebab itu, akurasi pada Class Emosi tidak baik dan datanya tidak cocok digunakan untuk mengklasifikasikan nilai mahasiswa akibat kurang spesifiknya emosi mahasiswa yang menggambarkan nilai yang didapatkan.''')


    ########### Nilai Emosi ############
    st.markdown("## 4. Penggunaan Hyperparameter Tuning pada Klasifikasi Nilai")
    st.markdown("Klasifikasi nilai emosi dengan hyperparameter tuning")
    st.markdown("#### Akurasi Model")

    # st.write(acc_ne_tun)
    acc_bar_plot(acc_ne_tun)
    st.write('''Pada visualisasi di atas, diketahui bahwa ketiga algoritma dapat mengklasifikasikan data Nilai Emosi dengan baik namun rendah pada algoritma Naive Bayes. Hal ini dapat dilihat dari akurasi yang ditunjukkan diagram batang, di mana akurasi berada di atas 80% selain algoritma Naive Bayes.''')

    st.markdown("#### Classification Report")
    with st.expander("Show Content"):
        st.table(cr_ne_tun.set_index('Klasifikasi'))

    st.markdown("#### Confusion Matrix")
    cm_ne_tun_NB['Class'] = delete_postfix_nilai(cm_ne_tun_NB)
    cm_ne_tun_SVM['Class'] = delete_postfix_nilai(cm_ne_tun_SVM)
    cm_ne_tun_KNN['Class'] = delete_postfix_nilai(cm_ne_tun_KNN)
    view_conf_matrix(cm_ne_tun_NB, cm_ne_tun_SVM, cm_ne_tun_KNN)
    st.markdown("<hr></hr>", unsafe_allow_html=True)


    ########### Perbandingan Klasifikasi dengan dan tanpa Hyperparameter Tuning ############
    st.markdown("## 5. Perbandingan Klasifikasi Nilai dengan dan tanpa Hyperparameter Tuning")
    st.markdown("Berdasarkan nilai emosi")

    # preprocessing dataframe
    acc_sum = pd.DataFrame()
    acc_sum = pd.concat([acc_sum, get_acc_summary('Tanpa Tuning', acc_ne_def)], ignore_index=True)
    acc_sum = pd.concat([acc_sum, get_acc_summary('Dengan Tuning', acc_ne_tun)], ignore_index=True)
    # st.write(acc_sum)

    # plotting
    bar_sum = alt.Chart(acc_sum).mark_bar().encode(
        x=alt.X("Algorithm", sort=acc_sum['Algorithm'].unique()),
        y='Accuracy', column=alt.Column('Classification', sort=acc_sum['Classification'].unique()),
        color='Algorithm', tooltip=['Classification','Algorithm','Accuracy']
        ).properties(width=130)
    st.altair_chart(bar_sum)

    st.write('''Pada ringkasan visualisasi di atas, didapatkan bahwa penggunaan Hyperparameter Tuning dapat meningkatkan performa algoritma klasifikasi. Hal ini disebabkan karena hyperparameter tuning dapat mengontrol proses pelatihan model sehingga didapatkan hyperparameter model dan hasil klasifikasi yang optimal. Diketahui, akurasi algoritma Support Vector Machine lebih mendominasi daripada dua algoritma lainnya. Dengan kata lain, algoritma Support Vector Machine cocok digunakan untuk dataset yang digunakan dalam proyek ini.''')
