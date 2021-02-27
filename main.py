import streamlit as st
import pandas as pd
import plotly.express as px

toilettes = pd.read_csv("data/sanisettesparis.csv", sep=';')
# create lat and lon column base on 'geo_point_2d' as float
toilettes["lat"] = toilettes['geo_point_2d'].str.split(",").str.get(0).astype(float)
toilettes["lon"] = toilettes['geo_point_2d'].str.split(",").str.get(1).astype(float)
# create arr column base on arrondissement as "1, 18, 5.."
arrondissements = toilettes['ARRONDISSEMENT'].astype(str)
arrondissements = arrondissements.str.replace("7500", "")
arrondissements = arrondissements.str.replace("750", "")
toilettes["arr"] = arrondissements
toilettes["arr"] = toilettes["arr"].astype(int)

'''
# Toilettes publiques de Paris
'''

# get all toilettes
total = toilettes.count().TYPE
st.write("Actuellement il y a plus de ", total, " toilettes publiques dans Paris")

col1, col2 = st.beta_columns([3, 1])
with col1:
    # display a map
    st.map(toilettes, zoom=11)

# st.write(toilettes[toilettes["arr"] == 5])

with col2:
    # Pie chart types of toilettes by arrondissement
    pieType = px.pie(toilettes,
                     values='arr',
                     names='TYPE',
                     hover_data=['arr'], labels={'arr': 'Arrondissements'},
                     color_discrete_sequence=px.colors.sequential.OrRd)
    pieType.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(pieType)

with st.beta_expander("En savoir plus :"):
    st.write("""
        Plus de 750 toilettes publiques et urinoirs sont installés dans Paris pour répondre aux exigences de la vie parisienne et des touristes. Leur accès est gratuit sur tout le territoire parisien. Voici plus d'informations sur un réseau unique au monde qui a su évoluer ces dernières années. 
    """)
    st.image("https://cdn.paris.fr/paris/2019/10/10/huge-646b1a47f1e5c66d4f269e59db5ae0a8.jpg")