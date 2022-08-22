import pandas as pd
import streamlit as st
import matplotlib as plt
import altair as alt
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from st_aggrid import AgGrid

def rule_desc(rule,desc):
    for i in range(len(rule)):
        LHS=str(rule["Antecedents"])
        desc.loc[i,"Rule"]=str(rule.loc[i,"Antecedents"])+' --> '+str(rule.loc[i,"Consequents"])
    return desc

rule_label=["Rule"]

def view_rule(PreTest, PostTest, Delta):
    with st.expander("Show Content"):
        st.write("Rule dengan Consequent dari PreTest")
        AgGrid(PreTest)
        st.write("Rule dengan Consequent dari PostTest")
        AgGrid(PostTest)
        st.write("Rule dengan Consequent dari Delta")
        AgGrid(Delta)

def asosiasi():
    ################################################################################################################
    ###########################################LIST DATAFRAME UNTUK ASOSIASI########################################
    with pd.ExcelFile('asosiasi/visualization.xlsx') as xls:
        ap_general = pd.read_excel(xls, 'ap_general')
        ap_combine = pd.read_excel(xls, 'ap_combine')
        ap_vis = pd.read_excel(xls, 'ap_vis')
        apriori_delta = pd.read_excel(xls, 'apriori_delta')
        apriori_general = pd.read_excel(xls, 'apriori_general')
        apriori_posttest = pd.read_excel(xls, 'apriori_posttest')
        apriori_pretest = pd.read_excel(xls, 'apriori_pretest')
        df_rule_fp = pd.read_excel(xls, 'df_rule_fp')
        fp_vis = pd.read_excel(xls, 'fp_vis')
        rule_ap_delta = pd.read_excel(xls, 'rule_ap_delta')
        rule_ap_general = pd.read_excel(xls, 'rule_ap_general')
        rule_ap_pretest = pd.read_excel(xls, 'rule_ap_pretest')
        rule_ap_posttest = pd.read_excel(xls, 'rule_ap_posttest')
        pie_pre = pd.read_excel(xls, 'pie_pre')
        pie_post = pd.read_excel(xls, 'pie_post')
        pie_delta = pd.read_excel(xls, 'pie_delta')


    #Time related
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
    
    #barchart general
    bar_ap_general = alt.Chart(ap_general).mark_bar().encode(
        x=alt.X('Consequents', type='nominal', sort=None),y='counts',
        tooltip=['Consequents', 'counts']).configure_mark(color='#7ec798').properties(width=800,height=600).interactive()
    st.altair_chart(bar_ap_general)
    st.markdown("Visualisasi diatas menunjukan frekuensi consequent yang muncul secara umum. Terlihat 'High Postest' memiliki jumlah kemunculan paling tinggi, diikuti 'Normal Stress' dan 'Moderate ESF'.")

    st.markdown("#### Rule yang diperoleh untuk RHS Pre Test, Post Test dan Delta Pada Algoritma Apriori")

    #Melihat Rule untuk RHS Pretest, posttest dan delta
    view_rule(rule_ap_pretest,rule_ap_posttest,rule_ap_delta)
    
    #pie chart
    st.markdown("##### Distribusi Consequent untuk Setiap PreTest, PostTest dan Delta")
    pie_1 = alt.Chart(pie_pre).mark_arc().encode(
        theta=alt.Theta(field="Jumlah", type="quantitative"),
        color=alt.Color(field="Consequents"),tooltip=['Consequents',"Jumlah"]
    )
    st.altair_chart(pie_1)

    pie_2 = alt.Chart(pie_post).mark_arc().encode(
        theta=alt.Theta(field="Jumlah", type="quantitative"),
        color=alt.Color(field="Consequents"),tooltip=['Consequents',"Jumlah"]
    )
    st.altair_chart(pie_2)
    
    pie_3 = alt.Chart(pie_delta).mark_arc().encode(
        theta=alt.Theta(field="Jumlah", type="quantitative"),
        color=alt.Color(field="Consequents"),tooltip=['Consequents',"Jumlah"]
    )
    st.altair_chart(pie_3)

    #barchart pretest, posttest dan delta
    st.markdown("##### Frekuensi consequent/RHS yang sering muncul")    
    bar_ap_vis = alt.Chart(ap_vis).mark_bar().encode(
        x=alt.X('Consequents', type='nominal', sort=None),y='Jumlah',
        tooltip=['Consequents', 'Jumlah']).configure_mark(color='#7ec798').properties(width=800,height=600).interactive()
    st.altair_chart(bar_ap_vis)

    #Scatter plot
    st.markdown("##### Hubungan antara Support dan Confidence")    
    scatter_ap_com  = alt.Chart(ap_combine).mark_point().encode(x=alt.Y('Support',scale=alt.Scale(zero=False)), y=alt.Y('Confidence',scale=alt.Scale(zero=False)),color=alt.Color('Lift:Q', scale=alt.Scale(scheme='orangered')),tooltip=['Antecedents','Consequents','Support', 'Confidence','Lift']).properties(width=800,height=600).interactive()
    st.altair_chart(scatter_ap_com)

    ################################################################################################################
    st.markdown("## 2. Algoritma FP-Growth")
    
    rule_fp_desc = pd.DataFrame(columns = rule_label)
    rule_fp_desc = rule_desc(df_rule_fp,rule_fp_desc)

    st.markdown("#### Rule yang diperoleh untuk RHS Pre Test, Post Test dan Delta Pada Algoritma FP-Growth")
    AgGrid(rule_fp_desc )

    #barchart pretest, posttest dan delta
    bar_fp_vis = alt.Chart(fp_vis).mark_bar().encode(
        x=alt.X('Consequents', type='nominal', sort=None),y='Jumlah',tooltip=['Consequents', 'Jumlah']).configure_mark(color='#7ec798').properties(width=800,height=600).interactive()
    st.altair_chart(bar_fp_vis)

    #Scatter plot
    scatter_fp_com  = alt.Chart(df_rule_fp).mark_point().encode(x=alt.X('Support',scale=alt.Scale(zero=False)), y=alt.Y('Confidence',scale=alt.Scale(zero=False)),color=alt.Color('Lift:Q', scale=alt.Scale(scheme='orangered')),tooltip=['Antecedents','Consequents','Support', 'Confidence','Lift']).properties(width=800,height=600).interactive()
    st.altair_chart(scatter_fp_com)



    st.markdown("## 3. Perbandingan Algoritma")

    #Line chart
    st.markdown("#### Perbandingan waktu eksekusi pada confidence dan support yang berbeda pada algoritma Apriori")
    line = alt.Chart(df_time_ap_1).mark_line().encode(x=alt.X('conf',scale=alt.Scale(zero=False)), y=alt.Y('elapsed_time',scale=alt.Scale(zero=False)),color = alt.Color('supp:N', scale=alt.Scale(scheme='set1')),tooltip=['conf','supp','elapsed_time','rule_count']).properties(width=800,height=600).interactive()
    st.altair_chart(line)

    st.markdown("#### Perbandingan waktu eksekusi pada jumlah antecedent yang berbeda")
    line = alt.Chart(df_time_ap_2).mark_line().encode(x=alt.X('n_len:N',scale=alt.Scale(zero=False)), y=alt.Y('elapsed_time',scale=alt.Scale(zero=False)),tooltip=['conf','supp','elapsed_time','rule_count']).configure_mark(color='#ffa06b').properties(width=800,height=600).interactive()
    st.altair_chart(line)

    st.markdown("#### Perbandingan waktu eksekusi pada confidence dan support yang berbeda pada algoritma FP-Growth")
    line = alt.Chart(df_time_fp).mark_line().encode(x=alt.X('conf',scale=alt.Scale(zero=False)), y=alt.Y('elapsed_time',scale=alt.Scale(zero=False)),color = alt.Color('supp:N', scale=alt.Scale(scheme='set1')),tooltip=['conf','supp','elapsed_time','rule_count']).properties(width=800,height=600).interactive()
    st.altair_chart(line)

    ################################################################################################################
    ################################################################################################################