import pandas as pd
import streamlit as st
import matplotlib as plt
import altair as alt
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
#from st_aggrid import AgGrid

def rule_desc(rule,desc):
    for i in range(len(rule)):
        LHS=str(rule["Antecedents"])
        desc.loc[i,"Rule"]=str(rule.loc[i,"Antecedents"])+' --> '+str(rule.loc[i,"Consequents"])
    return desc

rule_label=["Rule"]

def view_rule(PreTest, PostTest, Delta):
    with st.expander("Show Content"):
        PreTest=PreTest.set_index(PreTest.columns[0])
        PostTest=PostTest.set_index(PostTest.columns[0])
        Delta=Delta.set_index(Delta.columns[0])
        st.write("Rule dengan Consequent dari PreTest")
        st.write(PreTest)
        st.write("Rule dengan Consequent dari PostTest")
        st.write(PostTest)
        st.write("Rule dengan Consequent dari Delta")
        st.dataframe(Delta)
        #st.write(Delta.assign(hack='').set_index('hack'))

def asosiasi():
    ################################################################################################################
    ###########################################LIST DATAFRAME UNTUK ASOSIASI########################################
    with pd.ExcelFile('asosiasi/visualization.xlsx') as xls:
        ap_general = pd.read_excel(xls, 'ap_general')
        ap_pretest = pd.read_excel(xls, 'ap_pretest')
        ap_posttest = pd.read_excel(xls, 'ap_posttest')
        ap_delta = pd.read_excel(xls, 'ap_delta')

        rule_ap_general = pd.read_excel(xls, 'rule_ap_general')
        rule_ap_pretest = pd.read_excel(xls, 'rule_ap_pretest')
        rule_ap_posttest = pd.read_excel(xls, 'rule_ap_posttest')
        rule_ap_delta = pd.read_excel(xls, 'rule_ap_delta')

        fp_general = pd.read_excel(xls, 'fp_general')
        fp_pretest = pd.read_excel(xls, 'fp_pretest')
        fp_posttest = pd.read_excel(xls, 'fp_posttest')
        fp_delta = pd.read_excel(xls, 'fp_delta')

        rule_fp_general = pd.read_excel(xls, 'rule_fp_general')
        rule_fp_pretest = pd.read_excel(xls, 'rule_fp_pretest')
        rule_fp_posttest = pd.read_excel(xls, 'rule_fp_posttest')
        rule_fp_delta = pd.read_excel(xls, 'rule_fp_delta')

        ap_combination = pd.read_excel(xls, 'ap_combination')
        fp_combination = pd.read_excel(xls, 'fp_combination')

        ap_vis = pd.read_excel(xls, 'ap_vis')
        fp_vis = pd.read_excel(xls, 'fp_vis')
        df_cmp = pd.read_excel(xls, 'df_cmp')
    ################################################################################################################

    ################################################################################################################
    ################################################# BAGIAN HALAMAN ###############################################
    st.markdown("<h1 style='text-align: center; color: system;'>---Asosiasi---</h1>", unsafe_allow_html=True)
    st.sidebar.markdown("# Asosiasi")
    st.sidebar.markdown("## 195150201111034")
    st.sidebar.markdown("## Aldi Fianda Putra")

    st.markdown("## 1. Algoritma Apriori")
    st.markdown("##### Rule yang diperoleh Secara Umum")

    #tabel secara umum atau keseluruhan
    rule_ap_general=rule_ap_general.set_index(rule_ap_general.columns[0])
    st.write(rule_ap_general)

    st.markdown("##### Frekuensi consequent/RHS yang sering muncul")
    
    #barchart general
    bar_ap_general = alt.Chart(ap_general).mark_bar().encode(
        x=alt.X('Consequents', type='nominal', sort=None),y='counts',
        tooltip=['Consequents', 'counts']).configure_mark(color='#85bbdc').properties(width=800,height=600).interactive()
    st.altair_chart(bar_ap_general)
    st.markdown("Visualisasi diatas menunjukan frekuensi consequent yang muncul secara umum. Terlihat 'High Postest' memiliki jumlah kemunculan paling tinggi, diikuti 'Normal Stress' dan 'Moderate ESF'.")

    st.markdown("#### Rule yang diperoleh untuk RHS Pre Test, Post Test dan Delta Pada Algoritma Apriori")
    #Melihat Rule untuk RHS Pretest, posttest dan delta
    view_rule(rule_ap_pretest,rule_ap_posttest,rule_ap_delta)
    
    #pie chart
    st.markdown("##### Distribusi Consequent untuk Setiap PreTest, PostTest dan Delta")
    pie_ap_pre = alt.Chart(ap_pretest).mark_arc().encode(
        theta=alt.Theta(field="counts", type="quantitative"),
        color=alt.Color(field="Consequents",scale=alt.Scale(scheme='blues')),tooltip=['Consequents',"counts"]
    )
    st.altair_chart(pie_ap_pre)

    pie_ap_pos = alt.Chart(ap_posttest).mark_arc().encode(
        theta=alt.Theta(field="counts", type="quantitative"),
        color=alt.Color(field="Consequents",scale=alt.Scale(scheme='blues')),tooltip=['Consequents',"counts"]
    )
    st.altair_chart(pie_ap_pos)
    
    pie_ap_dlt = alt.Chart(ap_delta).mark_arc().encode(
        theta=alt.Theta(field="counts", type="quantitative"),
        color=alt.Color(field="Consequents",scale=alt.Scale(scheme='blues')),tooltip=['Consequents',"counts"]
    )
    st.altair_chart(pie_ap_dlt)

    #barchart pretest, posttest dan delta
    st.markdown("##### Frekuensi consequent/RHS yang sering muncul")    
    bar_ap_vis = alt.Chart(ap_vis).mark_bar().encode(
        x=alt.X('Consequents', type='nominal', sort=None),y='counts',
        tooltip=['Consequents', 'counts']).configure_mark(color='#85bbdc').properties(width=800,height=600).interactive()
    st.altair_chart(bar_ap_vis)

    #Scatter plot
    st.markdown("##### Hubungan antara Support dan Confidence")    
    scatter_ap_com  = alt.Chart(ap_combination).mark_point().encode(x=alt.Y('Support',scale=alt.Scale(zero=False)), y=alt.Y('Confidence',scale=alt.Scale(zero=False)),color=alt.Color('Lift:Q', scale=alt.Scale(scheme='blues')),tooltip=['Antecedents','Consequents','Support', 'Confidence','Lift']).properties(width=800,height=600).interactive()
    st.altair_chart(scatter_ap_com)

    ################################################################################################################
    st.markdown("## 2. Algoritma FP-Growth")
    st.markdown("##### Rule yang diperoleh Secara Umum")

    #tabel secara umum atau keseluruhan
    rule_fp_general=rule_fp_general.set_index(rule_fp_general.columns[0])
    st.write(rule_fp_general)

    st.markdown("##### Frekuensi consequent/RHS yang sering muncul")
    
    #barchart general
    bar_fp_general = alt.Chart(fp_general).mark_bar().encode(
        x=alt.X('Consequents', type='nominal', sort=None),y='counts',
        tooltip=['Consequents', 'counts']).configure_mark(color='#7cc47e').properties(width=800,height=600).interactive()
    st.altair_chart(bar_fp_general)
    st.markdown("Tampilan diatas adalah persebaran dari Consequent untuk algoritma FP-Growth yang diperoleh pada proses ekstraksi untuk mengambil rule yang consequentnya adalah semua yang memenuhi confidence dan support minimal tanpa dibatasi apakah consequent tersebut hanya terdapat pada pretest, posttest atau delta saja. ")


    st.markdown("#### Rule yang diperoleh untuk RHS Pre Test, Post Test dan Delta Pada Algoritma FP-Growth")

    #Melihat Rule untuk RHS Pretest, posttest dan delta
    view_rule(rule_fp_pretest,rule_fp_posttest,rule_fp_delta)

    #pie chart
    st.markdown("##### Distribusi Consequent untuk Setiap PreTest, PostTest dan Delta")
    pie_fp_pre = alt.Chart(fp_pretest).mark_arc().encode(
        theta=alt.Theta(field="counts", type="quantitative"),
        color=alt.Color(field="Consequents",scale=alt.Scale(scheme='greens')),tooltip=['Consequents',"counts"]
    )
    st.altair_chart(pie_fp_pre)

    pie_fp_pos = alt.Chart(fp_posttest).mark_arc().encode(
        theta=alt.Theta(field="counts", type="quantitative"),
        color=alt.Color(field="Consequents",scale=alt.Scale(scheme='greens')),tooltip=['Consequents',"counts"]
    )
    st.altair_chart(pie_fp_pos)
    
    pie_fp_dlt = alt.Chart(fp_delta).mark_arc().encode(
        theta=alt.Theta(field="counts", type="quantitative"),
        color=alt.Color(field="Consequents",scale=alt.Scale(scheme='greens')),tooltip=['Consequents',"counts"]
    )
    st.altair_chart(pie_fp_dlt)
    st.markdown("""Tampilan pie chart yang diperoleh untuk algoritma FP-Growth kurang lebih memiliki hasil yang sama dengan Apriori. Terlihat High PreTest, High PostTest dan Positive Delta merupakan label yang mayoritas muncul di masing-masing fiturnya. Moderate PreTest dan Negative Delta merupakan label minoritas yang muncul pada PreTest dan Delta. 
    Sedangkan untuk PostTest juga tidak terdapat label minor lainnya yang muncul.""")

    #barchart pretest, posttest dan delta
    bar_fp_vis = alt.Chart(fp_vis).mark_bar().encode(
        x=alt.X('Consequents', type='nominal', sort=None),y='counts',tooltip=['Consequents', 'counts']).configure_mark(color='#7cc47e').properties(width=800,height=600).interactive()
    st.altair_chart(bar_fp_vis)
    st.markdown("Tampilan bar chart diatas adalah tampilan perbandingan jumlah masing-masing consequent yang dihasilkan dari algoritma FP-Growth untuk fitur PreTest, PostTest, dan Delta.")

    #Scatter plot
    scatter_fp_com  = alt.Chart(fp_combination).mark_point().encode(x=alt.X('Support',scale=alt.Scale(zero=False)), y=alt.Y('Confidence',scale=alt.Scale(zero=False)),color=alt.Color('Lift:Q', scale=alt.Scale(scheme='greens')),tooltip=['Antecedents','Consequents','Support', 'Confidence','Lift']).properties(width=800,height=600).interactive()
    st.altair_chart(scatter_fp_com)
    st.markdown("""Tampilan diatas adalah tampilan relasi antara Support dengan Confidence pada rule yang diperoleh untuk label dari PreTest, PostTest dan Delta yang sudah digabungkan pada algoritma FP-Growth. 
    Terlihat pada scatter plot diatas memiliki hasil yang mirip dengan algoritma apriori dimana nilai lift cenderung tinggi pada item dengan support 0.05 dan confidence antara 0.47 hingga 0.6 lebih. Pada item dengan support dan confidence tersebut diperoleh lift yang melebihi 2.2 yang berarti antecedent dan consequent dari item tersebut memiliki relasi yang kuat.""")
    ################################################################################################################
    st.markdown("## 3. Perbandingan Algoritma")
    
    #barchart perbandingan waktu eksekusi
    st.markdown("##### Perbandingan waktu eksekusi antara dua algoritma")
    bar_time_cmp = alt.Chart(df_cmp).mark_bar().encode(
        x=alt.X('Algorithm', type='nominal', sort=None),y='Execution Time',tooltip=['Algorithm', 'Execution Time']).configure_mark(color='#85bbdc').properties(width=800,height=600).interactive()
    st.altair_chart(bar_time_cmp)
    st.markdown("Tampilan diatas adalah perbandingan waktu eksekusi antara algoritma Apriori dengan FP-Growth, dimana parameternya sama yakni minimal support sebesar 0.05, minimal confidence sebesar 0.1, dan lift sebesar 1. Waktu eksekusi FP-Growth lebih singkat dibandingkan FP-Growth yakni hanya sekitar 1 detik saja. Sedangkan algoritma Apriori memakan waktu eksekusi sebesar 1.7 detik lebih.")
    #barchart perbandingan rule
    st.markdown("##### Perbandingan Rule yang diperoleh Secara Umum")
    bar_time_cmp = alt.Chart(df_cmp).mark_bar().encode(
        x=alt.X('Algorithm', type='nominal', sort=None),y='Rule General',tooltip=['Algorithm', 'Rule General']).configure_mark(color='#7cc47e').properties(width=800,height=600).interactive()
    st.altair_chart(bar_time_cmp)
    st.markdown("Tampilan diatas menunjukan perbandingan jumlah rule yang diperoleh dari algoritma Apriori dengan FP-Growth. Dengan menggunakan nilai support, confidence dan lift yang sama maka diperoleh jumlah rule yang sama.")
    ################################################################################################################