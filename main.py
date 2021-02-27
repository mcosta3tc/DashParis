import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


toilettes = pd.read_csv("data/sanisettesparis.csv", sep=';')

'''
# Toilettes publiques de Paris
'''

total = toilettes.count().TYPE
st.write("Actuellement il y a plus de ", total ," toilettes publiques dans Paris")

arrondissements = toilettes['ARRONDISSEMENT']

st.write(arrondissements)

toilettes["lat"] = toilettes['geo_point_2d'].str.split(",").str.get(0)
toilettes["lon"] = toilettes['geo_point_2d'].str.split(",").str.get(1)

st.write(toilettes)

st.map(toilettes)

#st.write(toilettes["Latitude"])
#st.write(toilettes["Longitude"])



#status = toilettes.groupby(pd.Grouper(key="ARRONDISSEMENT")).mean().round(0)
#st.write(status)



#fig = px.bar(toilettes, x='ARRONDISSEMENT', y='STATUT', orientation='h')
#st.write(fig)