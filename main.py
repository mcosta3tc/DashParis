import streamlit as st
import pandas as pd
import plotly.express as px

toilettes = pd.read_csv("data/sanisettesparis.csv", sep=';')


'''
# Toilettes publiques de Paris
'''

# get all toilettes
total = toilettes.count().TYPE
st.write("Actuellement il y a plus de ", total, " toilettes publiques dans Paris")
# create lat and lon column base on 'geo_point_2d' as float
toilettes["lat"] = toilettes['geo_point_2d'].str.split(",").str.get(0).astype(float)
toilettes["lon"] = toilettes['geo_point_2d'].str.split(",").str.get(1).astype(float)
st.map(toilettes, zoom=11)

# create arr column base on arrondissement as "1, 18, 5.."
arrondissements = toilettes['ARRONDISSEMENT'].astype(str)
arrondissements = arrondissements.str.replace("7500", "")
arrondissements = arrondissements.str.replace("750", "")
toilettes["arr"] = arrondissements
toilettes["arr"] = toilettes["arr"].astype(int)

# st.write(toilettes[toilettes["arr"] == 5])

#Pie chart types of toilettes by arrondissement
pieType = px.pie(toilettes,
                 values='arr',
                 names='TYPE',
                 hover_data=['arr'], labels={'arr':'Arrondissements'},
                 color_discrete_sequence=px.colors.sequential.OrRd)
pieType.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(pieType)
