import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk


@st.cache
def get_data():
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
    return toilettes


data = get_data()

'''
# Toilettes publiques de Paris
'''

# get all toilettes
total = data.count().TYPE
st.write("Actuellement il y a plus de ", total, " toilettes publiques dans Paris :toilet:")

with st.beta_container():
    col1, col2 = st.beta_columns([5, 1])
    with col1:
        # filter data
        arr_to_filter = st.slider('Choisir un arrondissement', 1, 20, 5)
        filtered_data = data[data['arr'] == arr_to_filter]
        # display a map
        st.map(
            filtered_data,
            zoom=12.3
        )
    with col2:
        # Pie chart types of toilettes by arrondissement
        pieType = px.pie(
            filtered_data,
            title='Moyennes des types toilettes présentes sur cet arrondissement',
            values='arr',
            names='TYPE',
            hover_data=['arr'], labels={'arr': 'Arrondissement ', 'TYPE': 'Type de Toilette '},
            color_discrete_sequence=px.colors.sequential.OrRd
        )
        pieType.update_traces(textposition='inside', textinfo='percent+label')
        pieType.update_layout(showlegend=False)
        st.plotly_chart(pieType)

        # Expander with image and text
    with st.beta_expander("En savoir plus"):
        col1, col2 = st.beta_columns([3, 3])
        with col1:
            st.image("https://cdn.paris.fr/paris/2019/10/10/huge-646b1a47f1e5c66d4f269e59db5ae0a8.jpg")
        with col2:
            st.write("""
                 Plus de 750 toilettes publiques et urinoirs sont installés dans Paris pour répondre aux exigences de la vie parisienne et des touristes. Leur accès est gratuit sur tout le territoire parisien. [En savoir plus] (https://www.paris.fr/pages/les-sanisettes-2396) 
             """)

st.write(filtered_data)

st.write(filtered_data.groupby("TYPE").count())
