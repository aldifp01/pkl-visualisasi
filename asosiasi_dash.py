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

        df_supp_cmp = pd.read_excel(xls, 'df_supp_cmp')
        df_conf_cmp = pd.read_excel(xls, 'df_conf_cmp')
        df_lift_cmp = pd.read_excel(xls, 'df_lift_cmp')
    ################################################################################################################

    ################################################################################################################
    ################################################# BAGIAN HALAMAN ###############################################
    st.markdown("<h1 style='text-align: center; color: system;'>---Asosiasi---</h1>", unsafe_allow_html=True)
    st.sidebar.markdown("# Asosiasi")
    st.sidebar.markdown("## 195150201111034")
    st.sidebar.markdown("## Aldi Fianda Putra")

    st.markdown("<hr><hr></hr></hr>", unsafe_allow_html=True)
    st.markdown("Pada asosiasi, digunakan 2 algoritma machine learning yang akan dibandingkan performanya:")
    st.markdown("1. Apriori\n2. Frequent Pattern Growth")

    st.markdown("<hr></hr>", unsafe_allow_html=True)
    st.markdown("## 1. Algoritma Apriori")
    st.markdown("##### Rule yang diperoleh Secara Umum")

    #tabel secara umum atau keseluruhan
    rule_ap_general=rule_ap_general.set_index(rule_ap_general.columns[0])
    st.write(rule_ap_general)

    st.markdown("<hr></hr>", unsafe_allow_html=True)
    st.markdown("##### Frekuensi consequent/RHS yang sering muncul")
    
    #barchart general
    bar_ap_general = alt.Chart(ap_general).mark_bar().encode(
        x=alt.X('Consequents', type='nominal', sort=None),y='counts',
        tooltip=['Consequents', 'counts']).configure_mark(color='#1f77b4').properties(width=800,height=600).interactive()
    st.altair_chart(bar_ap_general)
    st.markdown("##### Penjelasan:")
    st.markdown("""Tampilan diatas adalah persebaran dari Consequent yang diperoleh pada proses ekstraksi untuk mengambil 
    rule yang consequentnya adalah semua yang memenuhi confidence dan support minimal tanpa dibatasi apakah consequent tersebut 
    hanya terdapat pada pretest, posttest atau delta saja.""")

    st.markdown("<hr></hr>", unsafe_allow_html=True)
    st.markdown("#### Rule yang diperoleh untuk RHS Pre Test, Post Test dan Delta Pada Algoritma Apriori")
    #Melihat Rule untuk RHS Pretest, posttest dan delta
    view_rule(rule_ap_pretest,rule_ap_posttest,rule_ap_delta)
    
    #pie chart
    st.markdown("<hr></hr>", unsafe_allow_html=True)
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
    st.markdown("##### Penjelasan:")
    st.markdown("""Tampilan pie chart diatas adalah untuk melihat persentase dari label yang memenuhi syarat minimal support, confidence dan lift. 
    Terlihat High PreTest, High PostTest dan Positive Delta merupakan label yang mayoritas muncul di masing-masing fiturnya. Moderate PreTest dan Negative 
    Delta merupakan label minoritas yang muncul pada PreTest dan Delta. Sedangkan untuk PostTest tidak terdapat label minor lainnya yang muncul.""")

    st.markdown("<hr></hr>", unsafe_allow_html=True)
    #barchart pretest, posttest dan delta
    st.markdown("##### Frekuensi consequent/RHS yang sering muncul")    
    bar_ap_vis = alt.Chart(ap_vis).mark_bar().encode(
        x=alt.X('Consequents', type='nominal', sort=None),y='counts',
        tooltip=['Consequents', 'counts']).configure_mark(color='#1f77b4').properties(width=800,height=600).interactive()
    st.altair_chart(bar_ap_vis)
    st.markdown("##### Penjelasan:")
    st.markdown("""Tampilan bar chart diatas adalah tampilan perbandingan jumlah masing-masing consequent yang dihasilkan dari algoritma Apriori 
    untuk fitur PreTest, PostTest, dan Delta.""")

    st.markdown("<hr></hr>", unsafe_allow_html=True)
    #Scatter plot
    st.markdown("##### Hubungan antara Support dan Confidence")    
    scatter_ap_com  = alt.Chart(ap_combination).mark_point().encode(x=alt.Y('Support',scale=alt.Scale(zero=False)), y=alt.Y('Confidence',scale=alt.Scale(zero=False)),color=alt.Color('Lift:Q', scale=alt.Scale(scheme='blues')),tooltip=['Antecedents','Consequents','Support', 'Confidence','Lift']).properties(width=800,height=600).interactive()
    st.altair_chart(scatter_ap_com)
    st.markdown("##### Penjelasan:")
    st.markdown("""Tampilan diatas adalah tampilan relasi antara Support dengan Confidence pada rule yang diperoleh untuk label dari PreTest, 
    PostTest dan Delta yang sudah digabungkan pada algoritma apriori. Terlihat pada scatter plot diatas nilai lift cenderung tinggi pada item 
    dengan support 0.05 dan confidence antara 0.47 hingga 0.6 lebih. Pada item dengan support dan confidence tersebut diperoleh lift yang melebihi 
    2.2 yang berarti antecedent dan consequent dari item tersebut memiliki relasi yang kuat.""")




    ################################################################################################################
    st.markdown("<hr></hr>", unsafe_allow_html=True)
    st.markdown("## 2. Algoritma FP-Growth")
    st.markdown("##### Rule yang diperoleh Secara Umum")

    #tabel secara umum atau keseluruhan
    rule_fp_general=rule_fp_general.set_index(rule_fp_general.columns[0])
    st.write(rule_fp_general)

    st.markdown("##### Frekuensi consequent/RHS yang sering muncul")
    
    st.markdown("<hr></hr>", unsafe_allow_html=True)
    #barchart general
    bar_fp_general = alt.Chart(fp_general).mark_bar().encode(
        x=alt.X('Consequents', type='nominal', sort=None),y='counts',
        tooltip=['Consequents', 'counts']).configure_mark(color='#ff7f0e').properties(width=800,height=600).interactive()
    st.altair_chart(bar_fp_general)
    st.markdown("##### Penjelasan:")
    st.markdown("""Tampilan diatas adalah persebaran dari Consequent untuk algoritma FP-Growth yang diperoleh pada proses ekstraksi untuk mengambil 
    rule yang consequentnya adalah semua yang memenuhi confidence dan support minimal tanpa dibatasi apakah consequent tersebut hanya terdapat pada 
    pretest, posttest atau delta saja. """)

    st.markdown("<hr></hr>", unsafe_allow_html=True)
    st.markdown("#### Rule yang diperoleh untuk RHS Pre Test, Post Test dan Delta Pada Algoritma FP-Growth")

    #Melihat Rule untuk RHS Pretest, posttest dan delta
    view_rule(rule_fp_pretest,rule_fp_posttest,rule_fp_delta)

    st.markdown("<hr></hr>", unsafe_allow_html=True)
    #pie chart
    st.markdown("##### Distribusi Consequent untuk Setiap PreTest, PostTest dan Delta")
    pie_fp_pre = alt.Chart(fp_pretest).mark_arc().encode(
        theta=alt.Theta(field="counts", type="quantitative"),
        color=alt.Color(field="Consequents",scale=alt.Scale(scheme='oranges')),tooltip=['Consequents',"counts"]
    )
    st.altair_chart(pie_fp_pre)

    pie_fp_pos = alt.Chart(fp_posttest).mark_arc().encode(
        theta=alt.Theta(field="counts", type="quantitative"),
        color=alt.Color(field="Consequents",scale=alt.Scale(scheme='oranges')),tooltip=['Consequents',"counts"]
    )
    st.altair_chart(pie_fp_pos)
    
    pie_fp_dlt = alt.Chart(fp_delta).mark_arc().encode(
        theta=alt.Theta(field="counts", type="quantitative"),
        color=alt.Color(field="Consequents",scale=alt.Scale(scheme='oranges')),tooltip=['Consequents',"counts"]
    )
    st.altair_chart(pie_fp_dlt)
    st.markdown("##### Penjelasan:")
    st.markdown("""Tampilan pie chart yang diperoleh untuk algoritma FP-Growth kurang lebih memiliki hasil yang sama dengan Apriori. Terlihat High PreTest, 
    High PostTest dan Positive Delta merupakan label yang mayoritas muncul di masing-masing fiturnya. Moderate PreTest dan Negative Delta merupakan label 
    minoritas yang muncul pada PreTest dan Delta. Sedangkan untuk PostTest juga tidak terdapat label minor lainnya yang muncul.""")

    st.markdown("<hr></hr>", unsafe_allow_html=True)
    # Visualisasi perbadngindan consequent pada pretest, posttest dan delta
    st.markdown("##### Frekuensi consequent/RHS yang sering muncul")
    bar_fp_vis = alt.Chart(fp_vis).mark_bar().encode(
        x=alt.X('Consequents', type='nominal', sort=None),y='counts',tooltip=['Consequents', 'counts']).configure_mark(color='#ff7f0e').properties(width=800,height=600).interactive()
    st.altair_chart(bar_fp_vis)
    st.markdown("Tampilan bar chart diatas adalah tampilan perbandingan jumlah masing-masing consequent yang dihasilkan dari algoritma FP-Growth untuk fitur PreTest, PostTest, dan Delta.")

    st.markdown("<hr></hr>", unsafe_allow_html=True)
    # Scatter plot relasi Support dan Confidence
    st.markdown("##### Hubungan antara Support dan Confidence")    
    scatter_fp_com  = alt.Chart(fp_combination).mark_point().encode(x=alt.X('Support',scale=alt.Scale(zero=False)), y=alt.Y('Confidence',scale=alt.Scale(zero=False)),color=alt.Color('Lift:Q', scale=alt.Scale(scheme='oranges')),tooltip=['Antecedents','Consequents','Support', 'Confidence','Lift']).properties(width=800,height=600).interactive()
    st.altair_chart(scatter_fp_com)
    st.markdown("##### Penjelasan:")
    st.markdown("""Tampilan diatas adalah tampilan relasi antara Support dengan Confidence pada rule yang diperoleh untuk label dari PreTest, PostTest dan Delta yang sudah 
    digabungkan pada algoritma FP-Growth. Terlihat pada scatter plot diatas memiliki hasil yang mirip dengan algoritma apriori dimana nilai lift 
    cenderung tinggi pada item dengan support 0.05 dan confidence antara 0.47 hingga 0.6 lebih. Pada item dengan support dan confidence tersebut 
    diperoleh lift yang melebihi 2.2 yang berarti antecedent dan consequent dari item tersebut memiliki relasi yang kuat.""")
    
    


    ################################################################################################################
    st.markdown("## 3. Evaluasi Algoritma Apriori dan FP-Growth")

    st.markdown("<hr></hr>", unsafe_allow_html=True)
    # Barchart perbandingan waktu eksekusi
    st.markdown("##### Perbandingan waktu eksekusi antara dua algoritma")
    bar_time_cmp = alt.Chart(df_cmp).mark_bar().encode(
        x=alt.X('Algorithm', type='nominal', sort=None),y='Execution Time',tooltip=['Algorithm', 'Execution Time']).configure_mark(color='#1f77b4').properties(width=500,height=500).interactive()
    st.altair_chart(bar_time_cmp)
    st.markdown("##### Penjelasan:")
    st.markdown("""Tampilan diatas adalah perbandingan waktu eksekusi antara algoritma Apriori dengan FP-Growth, dimana parameternya sama yakni minimal 
    support sebesar 0.05, minimal confidence sebesar 0.1, dan lift sebesar 1. Waktu eksekusi FP-Growth lebih singkat dibandingkan FP-Growth yakni hanya 
    sekitar 1 detik saja. Sedangkan algoritma Apriori memakan waktu eksekusi sebesar 1.7 detik lebih.""")
    
    st.markdown("<hr></hr>", unsafe_allow_html=True)
    # Barchart perbandingan rule
    st.markdown("##### Perbandingan Rule yang diperoleh secara Umum")
    bar_rule_cmp = alt.Chart(df_cmp).mark_bar().encode(
        x=alt.X('Algorithm', type='nominal', sort=None),y='Rule General',tooltip=['Algorithm', 'Rule General']).configure_mark(color='#ff7f0e').properties(width=500,height=500).interactive()
    st.altair_chart(bar_rule_cmp)
    st.markdown("##### Penjelasan:")
    st.markdown("""Tampilan diatas menunjukan perbandingan jumlah rule yang diperoleh dari algoritma Apriori dengan FP-Growth. Dengan menggunakan nilai support, 
    confidence dan lift yang sama maka diperoleh jumlah rule yang sama.""")
    
    
    st.markdown("<hr></hr>", unsafe_allow_html=True)
    df_supp_cmp=df_supp_cmp.set_index(df_supp_cmp.columns[0])
    df_conf_cmp=df_conf_cmp.set_index(df_conf_cmp.columns[0])
    df_lift_cmp=df_lift_cmp.set_index(df_lift_cmp.columns[0])
    st.write("Perbandingan Rule yang diperoleh dengan Support yang Berbeda")
    st.write(df_supp_cmp)
    st.write("Perbandingan Rule yang diperoleh dengan Confidence yang Berbeda")
    st.write(df_conf_cmp)
    st.write("Perbandingan Rule yang diperoleh dengan Lift yang Berbeda")
    st.write(df_lift_cmp)

    
    st.markdown("##### Perbandingan Rule yang diperoleh pada support,confidence, dan lift yang berbeda")
    line_supp_cmp = alt.Chart(df_supp_cmp).mark_line(point=alt.OverlayMarkDef(color="red")).encode(
        x='supp',
        y='rule_count',
        color='Method',tooltip=["supp","conf","lift","elapsed_time","rule_count"]
    ).properties(width=500,height=500).interactive()
    st.write("Perbandingan Rule yang diperoleh dengan Support yang Berbeda")
    st.altair_chart(line_supp_cmp)
    
    line_conf_cmp = alt.Chart(df_conf_cmp).mark_line(point=alt.OverlayMarkDef(color="red")).encode(
        x='conf',
        y='rule_count',
        color='Method',tooltip=["supp","conf","lift","elapsed_time","rule_count"]
    ).properties(width=500,height=500).interactive()
    st.write("Perbandingan Rule yang diperoleh dengan Confidence yang Berbeda")
    st.altair_chart(line_conf_cmp)

    line_lift_cmp = alt.Chart(df_lift_cmp).mark_line(point=alt.OverlayMarkDef(color="red")).encode(
        x='lift',
        y='rule_count',
        color='Method',tooltip=["supp","conf","lift","elapsed_time","rule_count"]
    ).properties(width=500,height=500).interactive()
    st.write("Perbandingan Rule yang diperoleh dengan Lift yang Berbeda")
    st.altair_chart(line_lift_cmp)
    
    st.markdown("##### Penjelasan:")
    st.markdown("""Tampilan diatas menunjukan perbandingan rule yang diperoleh ketika support, confidence dan lift memiliki nilai yang berbeda. 
    Terlihat bahwa pada algoritma FP-Growth rule yang diperoleh jauh lebih banyak dibandingkan Apriori, selain itu pada FP-Growth semakin rendah nilai
    parameternya semakin banyak rule yang diperoleh. Pada algoritma apriori untuk lift dan support yang berbeda hasil rulenya relatif stagnan dan tidak 
    ada perubahan, hanya pada confidence yang berbeda baru terdapat perbedaan jumlah rule meskipun tidak begitu signifikan.""")
    st.markdown("<hr></hr>", unsafe_allow_html=True)
    ################################################################################################################