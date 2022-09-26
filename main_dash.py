import pandas as pd
import streamlit as st
import matplotlib as plt
import altair as alt
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from st_aggrid import AgGrid
from collections import Counter


# fungsi melakukan counter jumlah instance kelas untuk 3 kategori
def get_count_3cat(df, col_name):
    dict_count = {}
    dict_count['Low'] = 0
    dict_count['Moderate'] = 0
    dict_count['High'] = 0

    dict_count.update(Counter(df[col_name]))
    return dict_count


# fungsi melakukan counter jumlah instance kelas untuk 5 kategori
def get_count_5cat(df, col_name):
    dict_count = {}
    dict_count['Normal'] = 0
    dict_count['Mild'] = 0
    dict_count['Moderate'] = 0
    dict_count['Severe'] = 0
    dict_count['Extremely Severe'] = 0

    dict_count.update(Counter(df[col_name]))
    return dict_count


# fungsi mencetak group bar plot
def bar_plot(count, col_list):
    # preprocessing dataframe agar dapat diplot dengan altair
    count.reset_index(inplace=True)
    count.rename(columns={count.columns[0]: "Regulasi Emosi"}, inplace = True)
    count_res = pd.DataFrame()
    for col_name in col_list:
        count_temp = count.copy(deep=True)[["Regulasi Emosi", col_name]].rename(columns={col_name:"Jumlah"})
        count_temp.insert(2, 'Label', col_name)
        count_res = pd.concat([count_res, count_temp], ignore_index=True)
    # st.write(count_res)

    # plotting
    bar_count = alt.Chart(count_res).mark_bar().encode(
        x=alt.X("Regulasi Emosi", sort=count_res['Regulasi Emosi'].unique()),
        y='Jumlah', column=alt.Column('Label', sort=count_res['Label'].unique()),
        color='Regulasi Emosi', tooltip=['Regulasi Emosi','Label','Jumlah']
        ).properties(width=130).interactive()
    st.altair_chart(bar_count)


def main_page():
    # Read Dataframe
    ## Classficcation Report 
    df = pd.read_excel('main/main_dataset.xlsx', sheet_name='df')
    df_aeq = pd.read_excel('main/main_dataset.xlsx', sheet_name='aeq')
    df_dass = pd.read_excel('main/main_dataset.xlsx', sheet_name='dass')
    df_erq = pd.read_excel('main/main_dataset.xlsx', sheet_name='erq')
    df_nilai = pd.read_excel('main/main_dataset.xlsx', sheet_name='nilai')

    st.markdown("<h1 style='text-align: center; color: system;'>---PRAKTIK KERJA LAPANGAN---</h1>", unsafe_allow_html=True)
    st.sidebar.markdown("## Anggota Kelompok:")
    st.sidebar.markdown("1. Aldi Fianda Putra\n2. Riski Darmawan\n3. Hasyir Daffa Ibrahim")
    st.markdown("<hr></hr><hr></hr>", unsafe_allow_html=True)

    st.markdown("## Dataset")
    st.write('''- Terdiri dari 4 instrumen:\n
    1. Achievement Emotion Questionnaire (AEQ-s)\n
    \tDibagi menjadi Class-Related Emotions dan Learning-Related Emotions\n
    \tMasing-masing mengevaluasi emosi positif dan emosi negatif
    2. Depression, Anxiety, and Stress Scale (DASS-21)\n
    3. Emotion Regulation Questionnaire (ERQ)\n
    4. Nilai Mahasiswa\n 
    \tDibagi menjadi Nilai Pre-test dan Post-test\n''')
    st.write('''
    - Sumber: Kuesioner Google Form\n
    - Responden: Mahasiswa Fakultas Ilmu Komputer, Universitas Brawijaya\n
    - Jumlah Data: {}'''.format(df.shape[0]))
    st.markdown("<hr></hr>", unsafe_allow_html=True)

    ########### Informasi Umum ############
    st.markdown("## Informasi Umum")

    ### Persentase Angkatan ###
    st.markdown("#### Persentase Angkatan Responden")

    # preprocessing dataframe
    angkatan = pd.DataFrame(Counter(df['Angkatan']), index=[0])
    angkatan = angkatan.transpose()
    angkatan.reset_index(inplace=True)
    angkatan.rename(columns= {'index':'Angkatan', 0:'Jumlah'}, inplace=True)
    # st.write(angkatan)

    # ploting
    pie_angk = alt.Chart(angkatan).mark_arc().encode(
        theta=alt.Theta(field='Jumlah', type='quantitative'),
        color=alt.Color(field='Angkatan', type='nominal'),
        tooltip=['Angkatan','Jumlah']
    )
    st.altair_chart(pie_angk)
    st.write('''Pada visualisasi di atas, diketahui bahwa partisipan atau responden terdiri dari mahasiswa Fakultas Ilmu Komputer Universitas Brawijaya angkatan 17 hingga 21. Partisipan didominasi oleh mahasiswa angkatan 20. Sedangkan angkatan 17 merupakan partisipan dengan jumlah paling sedikit.''')


    ### Persentase Kelas ###
    st.markdown("#### Persentase Kelas Responden")

    # preprocessing dataframe
    df_mk = df['Mata Kuliah'].copy(deep=True)
    df_mk = df_mk.replace(['PPM F'], 'PPM')
    df_mk = df_mk.replace(['IESI A'], 'IESI').replace(['IESI D'], 'IESI')
    df_mk = df_mk.replace(['ADSI B'], 'ADSI').replace(['ADSI E'], 'ADSI')
    df_mk = df_mk.replace(['DPSI C'], 'DPSI')
    df_mk = df_mk.replace(['DDAP E'], 'DDAP')
    df_mk = df_mk.replace(['DIMP A'], 'DIMP').replace(['DIMP C'], 'DIMP')
    # st.write(df_mk.unique())
    matakuliah = pd.DataFrame(Counter(df_mk), index=[0])
    matakuliah = matakuliah.transpose()
    matakuliah.reset_index(inplace=True)
    matakuliah.rename(columns= {'index':'Mata Kuliah', 0:'Jumlah'}, inplace=True)
    # st.write(matakuliah)

    # ploting
    pie_matakuliah = alt.Chart(matakuliah).mark_arc().encode(
        theta=alt.Theta(field='Jumlah', type='quantitative'),
        color=alt.Color(field='Mata Kuliah', type='nominal'),
        tooltip=['Mata Kuliah','Jumlah']
    )
    st.altair_chart(pie_matakuliah)
    st.write('''Pada visualisasi di atas, diketahui bahwa data tersebar dengan cukup baik. Hal ini dapat dilihat pada proporsi setiap kelas mata kuliah yang tidak terlalu sedikit dan tidak terlalu banyak. Untuk kelas yang lebih mendominasi kontribusi proyek ada pada kelas ADSI dan IESI.''')

    st.markdown("<hr></hr>", unsafe_allow_html=True)


    ########### Category ###########
    cat3 = ['Low', 'Moderate', 'High']
    cat5 = ['Normal', 'Mild', 'Moderate', 'Severe', 'Extremely Severe']


    ########### AEQ ############
    st.markdown("## Achievement Emotion Questionnaire (AEQ-s)")

    # mendapatkan data jumlah instance tiap kelas untuk divisualisasikan
    # emosi positif
    aeq_count_pos = pd.DataFrame()
    for col_name in df_aeq.iloc[:, [-4,-2]].columns:
        aeq_count_pos = pd.concat([aeq_count_pos, pd.DataFrame(get_count_3cat(df_aeq, col_name), index=[col_name])])
    # emosi negatif
    aeq_count_neg = pd.DataFrame()
    for col_name in df_aeq.iloc[:, [-3,-1]].columns:
        aeq_count_neg = pd.concat([aeq_count_neg, pd.DataFrame(get_count_3cat(df_aeq, col_name), index=[col_name])])
    # st.write(aeq_count_pos)
    # st.write(aeq_count_neg)
    
    # plotting
    st.markdown("#### Persebaran Data - Emosi Positif")
    bar_plot(aeq_count_pos, cat3)
    st.write('''Pada visualisasi di atas, diketahui bahwa mahasiswa cenderung memiliki emosi positif yang tinggi. Hal ini dapat diketahui dari jumlah data pada kategori high yang lebih banyak daripada dua kategori lainnya. Hal ini baik karena dapat diartikan dengan mahasiswa cenderung memiliki emosi positif saat di kelas dan saat pembelajaran berlangsung.''')
    st.markdown("#### Persebaran Data - Emosi Negatif")
    bar_plot(aeq_count_neg, cat3)
    st.write('''Pada visualisasi di atas, diketahui bahwa mahasiswa cenderung memiliki emosi negatif yang rendah. Hal ini dapat diketahui dari jumlah data pada kategori low yang lebih banyak daripada dua kategori lainya. Hal ini baik karena dapat diartikan dengan mahasiswa cenderung memiliki emosi positif saat di kelas dan saat pembelajaran berlangsung.''')


    st.markdown("<hr></hr>", unsafe_allow_html=True)


    ########### DASS ############
    st.markdown("## Depression, Anxiety, and Stress Scale (DASS-21)")
    st.markdown("#### Persebaran Data")

    # mendapatkan data jumlah instance tiap kelas untuk divisualisasikan
    dass_count = pd.DataFrame()
    for col_name in df_dass.iloc[:, -3:].columns:
        dass_count = pd.concat([dass_count, pd.DataFrame(get_count_5cat(df_dass, col_name), index=[col_name])])
    # st.write(dass_count)

    # plotting
    bar_plot(dass_count, cat5)

    st.write('''Pada visualisasi di atas, diketahui bahwa mahasiswa cenderung memiliki emosi yang positif. Sifat kuesioner DASS adalah mengukur emosi negatif, sehingga dapat diketahui bahwa mahasiswa sebagian besar memiliki emosi negatif yang normal. Mahasiswa dengan emosi negatif pada kategori mild ke atas cenderung lebih sedikit. ''')

    st.markdown("<hr></hr>", unsafe_allow_html=True)


    ########### ERQ ############
    st.markdown("## Emotion Regulation Questionnaire (ERQ)")
    st.markdown("#### Persebaran Data")

    # mendapatkan data jumlah instance tiap kelas untuk divisualisasikan
    erq_count = pd.DataFrame()
    for col_name in df_erq.iloc[:, -2:].columns:
        erq_count = pd.concat([erq_count, pd.DataFrame(get_count_3cat(df_erq, col_name), index=[col_name])])
    # st.write(erq_count)

    # plotting
    bar_plot(erq_count, cat3)

    st.write('''Pada visualisasi di atas, diketahui bahwa mahasiswa memiliki proporsi emosi positif dan negatif yang seimbang. Hal ini diketahui dari jumlah data pada kategori moderate yang dominan daripada dua kategoi yang lain. Sedangkan kategori high dan low cenderung sedikit.''')

    st.markdown("<hr></hr>", unsafe_allow_html=True)


    ########### Nilai ############
    st.markdown("## Nilai Mahasiswa")

    # preprocessing dataframe untuk menghilangkan postfix
    df_nilai.iloc[:, -3] = df_nilai.iloc[:, -3].replace(['High PreTest'], 'High').replace(['Moderate PreTest'], 'Moderate').replace(['Low PreTest'], 'Low')
    df_nilai.iloc[:, -2] = df_nilai.iloc[:, -2].replace(['High PostTest'], 'High').replace(['Moderate PostTest'], 'Moderate').replace(['Low PostTest'], 'Low')
    df_nilai.iloc[:, -1] = df_nilai.iloc[:, -1].replace(['Positive Delta'], 'Positive').replace(['Negative Delta'], 'Negative')
    # st.write(df_nilai)


    ### PreTest dan PostTest ###
    st.markdown("#### Persebaran Data - Nilai PreTest dan PostTest")

    # mendapatkan data jumlah instance tiap kelas untuk divisualisasikan
    nilai_count = pd.DataFrame()
    for col_name in df_nilai.iloc[:, -3:-1].columns:
        nilai_count = pd.concat([nilai_count, pd.DataFrame(get_count_3cat(df_nilai, col_name), index=[col_name])])
    # st.write(nilai_count)

    # preprocessing dataframe agar dapat diplot dengan altair
    nilai_count.reset_index(inplace=True)
    nilai_count.rename(columns={nilai_count.columns[0]: "Regulasi"}, inplace = True)
    count_res = pd.DataFrame()
    for col_name in cat3:
        count_temp = nilai_count.copy(deep=True)[["Regulasi", col_name]].rename(columns={col_name:"Jumlah"})
        count_temp.insert(2, 'Label', col_name)
        count_res = pd.concat([count_res, count_temp], ignore_index=True)
    # st.write(count_res)

    # plotting
    bar_count_nilai = alt.Chart(count_res).mark_bar().encode(
        x=alt.X("Regulasi", sort=count_res['Regulasi'].unique()),
        y='Jumlah', column=alt.Column('Label', sort=count_res['Label'].unique()),
        color='Regulasi', tooltip=['Regulasi','Label','Jumlah']
        ).properties(width=130).interactive()
    st.altair_chart(bar_count_nilai)

    st.write('''Pada visualisasi di atas, diketahui bahwa mahasiswa yang sudah memahami materi HTML dan CSS sebelum menggunakan platform HSS Learning sudah cukup banyak. Hal ini dapat dilihat pada jumlah data kategori high nilai pre-test yang sudah banyak. Kemudian, setelah menggunakan platform HSS Learning, pengetahuan mahasiswa cenderung terjadi peningkatan sehingga jumlah data kategori high nilai post-test lebih banyak daripada pre-test. Terdapat sejumlah mahasiswa yang tergolong dalam kategori moderate dan bahkan low. Namun, tidak ada mahasiswa yang tergolong dalam kategori low pada nilai post-test.''')


    ### Delta ###
    st.markdown("#### Persebaran Data - Perubahan Nilai (Delta)")

    # mendapatkan data jumlah instance tiap kelas untuk divisualisasikan
    delta_count = pd.DataFrame(Counter(df_nilai.iloc[:, -1]), index=['Delta'])
    # st.write(delta_count)

    # preprocessing dataframe agar dapat diplot dengan altair
    delta_count.reset_index(inplace=True)
    delta_count.rename(columns={delta_count.columns[0]: "Regulasi"}, inplace = True)
    count_res = pd.DataFrame()
    for col_name in ['Positive', 'Negative']:
        count_temp = delta_count.copy(deep=True)[["Regulasi", col_name]].rename(columns={col_name:"Jumlah"})
        count_temp.insert(2, 'Label', col_name)
        count_res = pd.concat([count_res, count_temp], ignore_index=True)
    # st.write(count_res)

    # plotting
    bar_count_delta = alt.Chart(count_res).mark_bar().encode(
        x=alt.X("Label", sort=count_res['Label'].unique()),
        y='Jumlah', color='Label', tooltip=['Regulasi','Label','Jumlah']
        ).properties(width=400).interactive()
    st.altair_chart(bar_count_delta)

    st.write('''Pada visualisasi di atas, diketahui bahwa perubahan nilai (delta) mahasiswa lebih banyak bersifat positif. Delta positif menandakan adanya peningkatan nilai atau setidaknya mahasiswa dapat mempertahankan nilainya setelah menggunakan platform HSS Learning. Sebaliknya, delta negatif menandakan adanya penurunan nilai setelah menggunakan platform HSS Learning. Dengan demikian, dapat disimpulkan bahwa setelah menggunakan platform ini, perubahan nilai mahasiswa cenderung bersifat positif.''')

