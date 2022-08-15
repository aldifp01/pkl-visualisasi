import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go


header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()

#ap_general = pd.read_csv('ap_general.csv')



with header:
    st.title("INI PRAKTIK KERJA LAPANGAN")

#with dataset:
#    st.header("AYONIMA")
#    st.bar_chart(ap_general)

df =pd.DataFrame({"source_number":[11199,11328,11287,32345,12342,1232,13456,123244,1235],
    "location":["loc1","loc2","loc3","loc1","loc1","loc2","loc3","loc2","loc1"],
    "category":["cat1","cat3","cat1","cat3","cat2","cat3","cat2","cat3","cat1"],
    })

columns = df.columns.tolist()
selected_columns = st.multiselect("select column", columns, default="location")
s = df[selected_columns[0]].str.strip().value_counts()

trace = go.Bar(x=s.index,y=s.values,showlegend = True)
layout = go.Layout(title = "test")
data = [trace]
fig = go.Figure(data=data,layout=layout)
st.plotly_chart(fig)

