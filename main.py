import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


toilettes = pd.read_csv("data/sanisettesparis.csv", sep=';')

'''
# Toilettes publiques de Paris
'''

# get all toilettes
total = toilettes.count().TYPE
st.write("Actuellement il y a plus de ", total ," toilettes publiques dans Paris")

#create lat and lon column base on 'geo_point_2d' as float
toilettes["lat"] = toilettes['geo_point_2d'].str.split(",").str.get(0).astype(float)
toilettes["lon"] = toilettes['geo_point_2d'].str.split(",").str.get(1).astype(float)
st.map(toilettes)

#create arr column base on arrondissement as "1, 18, 5.."
arrondissements = toilettes['ARRONDISSEMENT'].astype(str)
arrondissements = arrondissements.str.replace("7500", "")
arrondissements = arrondissements.str.replace("750", "")
toilettes["arr"] = arrondissements
toilettes["arr"] = toilettes["arr"].astype(int)

st.write(toilettes)


#st.write(toilettes["Latitude"])
#st.write(toilettes["Longitude"])



#status = toilettes.groupby(pd.Grouper(key="ARRONDISSEMENT")).mean().round(0)
#st.write(status)



#fig = px.bar(toilettes, x='ARRONDISSEMENT', y='STATUT', orientation='h')
#st.write(fig)