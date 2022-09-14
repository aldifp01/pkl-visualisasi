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
    acc_aeq = pd.read_excel('D:/UB/Materi/PKL/Dashboard/klasifikasi/classification_report.xlsx', sheet_name='aeq')
    acc_dass = pd.read_excel('D:/UB/Materi/PKL/Dashboard/klasifikasi/classification_report.xlsx', sheet_name='dass')
    acc_erq = pd.read_excel('D:/UB/Materi/PKL/Dashboard/klasifikasi/classification_report.xlsx', sheet_name='erq')
    acc_ne = pd.read_excel('D:/UB/Materi/PKL/Dashboard/klasifikasi/classification_report.xlsx', sheet_name='nilai_emosi')
    acc_ce = pd.read_excel('D:/UB/Materi/PKL/Dashboard/klasifikasi/classification_report.xlsx', sheet_name='class_emosi')

    ## Confusion Matrix Report
    cm_aeq_NB = pd.read_excel('D:/UB/Materi/PKL/Dashboard/klasifikasi/confmatrix_report.xlsx', sheet_name='aeq_NB')
    cm_aeq_SVM = pd.read_excel('D:/UB/Materi/PKL/Dashboard/klasifikasi/confmatrix_report.xlsx', sheet_name='aeq_SVM')
    cm_aeq_KNN = pd.read_excel('D:/UB/Materi/PKL/Dashboard/klasifikasi/confmatrix_report.xlsx', sheet_name='aeq_KNN')

    cm_dass_NB = pd.read_excel('D:/UB/Materi/PKL/Dashboard/klasifikasi/confmatrix_report.xlsx', sheet_name='dass_NB')
    cm_dass_SVM = pd.read_excel('D:/UB/Materi/PKL/Dashboard/klasifikasi/confmatrix_report.xlsx', sheet_name='dass_SVM')
    cm_dass_KNN = pd.read_excel('D:/UB/Materi/PKL/Dashboard/klasifikasi/confmatrix_report.xlsx', sheet_name='dass_KNN')

    cm_erq_NB = pd.read_excel('D:/UB/Materi/PKL/Dashboard/klasifikasi/confmatrix_report.xlsx', sheet_name='erq_NB')
    cm_erq_SVM = pd.read_excel('D:/UB/Materi/PKL/Dashboard/klasifikasi/confmatrix_report.xlsx', sheet_name='erq_SVM')
    cm_erq_KNN = pd.read_excel('D:/UB/Materi/PKL/Dashboard/klasifikasi/confmatrix_report.xlsx', sheet_name='erq_KNN')

    cm_ne_NB = pd.read_excel('D:/UB/Materi/PKL/Dashboard/klasifikasi/confmatrix_report.xlsx', sheet_name='ne_NB')
    cm_ne_SVM = pd.read_excel('D:/UB/Materi/PKL/Dashboard/klasifikasi/confmatrix_report.xlsx', sheet_name='ne_SVM')
    cm_ne_KNN = pd.read_excel('D:/UB/Materi/PKL/Dashboard/klasifikasi/confmatrix_report.xlsx', sheet_name='ne_KNN')

    cm_ce_NB = pd.read_excel('D:/UB/Materi/PKL/Dashboard/klasifikasi/confmatrix_report.xlsx', sheet_name='ce_NB')
    cm_ce_SVM = pd.read_excel('D:/UB/Materi/PKL/Dashboard/klasifikasi/confmatrix_report.xlsx', sheet_name='ce_SVM')
    cm_ce_KNN = pd.read_excel('D:/UB/Materi/PKL/Dashboard/klasifikasi/confmatrix_report.xlsx', sheet_name='ce_KNN')


    # st.markdown("# Klasifikasi")
    st.markdown("<h1 style='text-align: center; color: system;'>---Klasifikasi---</h1>", unsafe_allow_html=True)
    st.markdown("<hr></hr><hr></hr>", unsafe_allow_html=True)
    st.sidebar.markdown("# Klasifikasi")
    st.sidebar.markdown("## 195150200111039")
    st.sidebar.markdown("## Riski Darmawan")
    st.markdown("Pada klasifikasi, digunakan 3 algoritma machine learning yang akan dibandingkan performanya:")
    st.markdown("1. Naive Bayes\n2. Support Vector Machine\n3. K-Nearest Neighbor")
    st.markdown("<hr></hr>", unsafe_allow_html=True)


    ########### AEQ ############
    st.markdown("## 1. Achievement Emotion Questionnaire (AEQ-s)")
    st.markdown("#### Akurasi Model")

    # st.write(acc_aeq)
    acc_bar_plot(acc_aeq)
    st.write('''Pada visualisasi di atas, diketahui bahwa ketiga algoritma dapat mengklasifikasikan data AEQ dengan sangat baik. Hal ini dapat dilihat dari akurasi yang ditunjukkan diagram batang, di mana setidaknya akurasi berada di atas 90% bahkan mencapai 100% pada algoritma Support Vector Machine. Bagian Summary menunjukkan rata-rata akurasi algoritma terhadap data AEQ. Dari ketiga algoritma klasifikasi yang digunakan, diketahui bahwa Support Vector Machine memiliki akurasi yang paling tinggi dibandingkan dengan dua algoritma lainnya.''')
    
    st.markdown("#### Confusion Matrix")
    view_conf_matrix(cm_aeq_NB, cm_aeq_SVM, cm_aeq_KNN)
    st.markdown("<hr></hr>", unsafe_allow_html=True)


    ########### DASS ############
    st.markdown("## 2. Depression, Anxiety, and Stress Scale (DASS-21)")
    st.markdown("#### Akurasi Model")

    # st.write(acc_dass)
    acc_bar_plot(acc_dass)
    st.write('''Pada visualisasi di atas, diketahui bahwa ketiga algoritma dapat mengklasifikasikan data DASS dengan sangat baik. Namun, tidak cukup baik pada regulasi emosi Anxiety dimana algoritma Naive Bayes dan K-Nearest Neighbor mengalami penurunan akurasi yang cukup banyak. Bagian Summary menunjukkan rata-rata akurasi algoritma terhadap data DASS. Dari ketiga algoritma klasifikasi yang digunakan, diketahui bahwa Support Vector Machine memiliki akurasi yang paling tinggi dibandingkan dengan dua algoritma lainnya.''')

    st.markdown("#### Confusion Matrix")
    view_conf_matrix(cm_dass_NB, cm_dass_SVM, cm_dass_KNN)
    st.markdown("<hr></hr>", unsafe_allow_html=True)


    ########### ERQ ############
    st.markdown("## 3. Emotion Regulation Questionnaire (ERQ)")
    st.markdown("#### Akurasi Model")

    # st.write(acc_erq)
    acc_bar_plot(acc_erq)
    st.write('''Pada visualisasi di atas, diketahui bahwa ketiga algoritma dapat mengklasifikasikan data ERQ dengan sangat baik. Hal ini dapat dilihat dari akurasi yang ditunjukkan diagram batang, di mana setidaknya akurasi berada di atas 90% bahkan mencapai 100% pada algoritma Support Vector Machine. Bagian Summary menunjukkan rata-rata akurasi algoritma terhadap data ERQ. Dari ketiga algoritma klasifikasi yang digunakan, diketahui bahwa Support Vector Machine memiliki akurasi yang paling tinggi dibandingkan dengan dua algoritma lainnya. Algoritma Support Vector Machine dapat mengkalsifikasikan data ERQ dengan sempurna, sehingga didapatkan akurasi sebesar 100%.''')

    st.markdown("#### Confusion Matrix")
    view_conf_matrix(cm_erq_NB, cm_erq_SVM, cm_erq_KNN)
    st.markdown("<hr></hr>", unsafe_allow_html=True)


    ########### Nilai Emosi ############
    st.markdown("## 4. Nilai (1)")
    st.markdown("Berdasarkan nilai emosi")
    st.markdown("#### Akurasi Model")

    # st.write(acc_ne)
    acc_bar_plot(acc_ne)
    st.write('''Pada visualisasi di atas, diketahui bahwa ketiga algoritma dapat mengklasifikasikan data Nilai Emosi dengan cukup baik namun rendah pada algoritma Naive Bayes. Hal ini dapat dilihat dari akurasi yang ditunjukkan diagram batang, di mana setidaknya akurasi berada di atas 80% selain algoritma Naive Bayes. Bagian Summary menunjukkan rata-rata akurasi algoritma terhadap data Nilai Emosi. Dari ketiga algoritma klasifikasi yang digunakan, diketahui bahwa K-Nearest memiliki akurasi yang paling tinggi dibandingkan dengan dua algoritma lainnya, namun hanya berbeda sedikit dengan Support Vector Machine.''')

    st.markdown("### Confusion Matrix")
    cm_ne_NB['Class'] = delete_postfix_nilai(cm_ne_NB)
    cm_ne_SVM['Class'] = delete_postfix_nilai(cm_ne_SVM)
    cm_ne_KNN['Class'] = delete_postfix_nilai(cm_ne_KNN)
    view_conf_matrix(cm_ne_NB, cm_ne_SVM, cm_ne_KNN)
    st.markdown("<hr></hr>", unsafe_allow_html=True)


    ########### Klasifikasi Emosi ############
    st.markdown("## 5. Nilai (2)")
    st.markdown("Berdasarkan klasifikasi emosi")
    st.markdown("#### Akurasi Model")

    # st.write(acc_ce)
    acc_bar_plot(acc_ce)
    st.write('''Pada visualisasi di atas, diketahui bahwa ketiga algoritma dapat mengklasifikasikan data Class Emosi dengan akurasi rendah. Hal ini dapat dilihat dari akurasi yang ditunjukkan diagram batang, di mana akurasi tiap algoritma tidak ada yang mencapai 80%, bahkan hanya 50%. Hasil akurasi ini sangat rendah jika dibandingkan dengan klasifikasi nilai menggunakan data Nilai Emosi. Hal ini sangat dimungkinkan terjadi karena klasifikasi Class Emosi menggunakan data regulasi emosi secara langsung atau dengan kata lain generalisasi / kesimpulan dari emosi yang dimiliki mahasiswa. Sedangkan klasifikasi Nilai Emosi menggunakan data yang membentuk regulasi emosi mahasiswa sehingga data menjadi lebih banyak dan spesifik. Oleh sebab itu, akurasi pada Class Emosi tidak baik dan datanya tidak cocok digunakan untuk mengklasifikasikan nilai mahasiswa akibat kurang spesifiknya emosi mahasiswa yang menggambarkan nilai yang didapatkan.''')

    st.markdown("#### Confusion Matrix")
    cm_ce_NB['Class'] = delete_postfix_nilai(cm_ce_NB)
    cm_ce_SVM['Class'] = delete_postfix_nilai(cm_ce_SVM)
    cm_ce_KNN['Class'] = delete_postfix_nilai(cm_ce_KNN)
    view_conf_matrix(cm_ce_NB, cm_ce_SVM, cm_ce_KNN)
    st.markdown("<hr></hr>", unsafe_allow_html=True)

    
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

