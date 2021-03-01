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

# SIDEBAR
st.sidebar.title("Choisir un arrondissement")
arr_to_filter = st.sidebar.slider('Du 1er au 20e arrondissement de Paris', 1, 20, 5)
st.sidebar.write("Vous êtes dans le ", arr_to_filter, "arrondissement de Paris")
# filter data
filtered_data = data[data['arr'] == arr_to_filter]
# filtered map
st.sidebar.map(
    filtered_data,
    zoom=11.3
)

# MAIN CONTAINER

st.title("Les toilettes publiques à Paris")

# count of toilets
total = data.count().TYPE
st.write("Actuellement il y a plus de ", total, " toilettes publiques dans Paris :toilet:")

# Expander: image, txt, map
with st.beta_expander("En savoir plus"):
    # define equals column
    col1, col2 = st.beta_columns([3, 3])
    with col1:
        st.image("https://cdn.paris.fr/paris/2019/10/10/huge-646b1a47f1e5c66d4f269e59db5ae0a8.jpg")
    with col2:
        st.markdown("""
                     Plus de 750 toilettes publiques et urinoirs sont installés dans Paris pour répondre aux exigences de la vie parisienne et des touristes. Leur accès est gratuit sur tout le territoire parisien. [En savoir plus] (https://www.paris.fr/pages/les-sanisettes-2396) 
                 """)

    # general map of toilets in Paris
    # st.map(
    #     data,
    #     zoom=11,
    #     use_container_width=False
    # )

st.subheader("Type de toilettes dans le " + str(arr_to_filter) + "e")
# Pie chart types of toilettes by arrondissement
pieType = px.pie(
    filtered_data,
    values='arr',
    names='TYPE',
    hover_data=['arr'],
    labels={'arr': 'Arrondissement ', 'TYPE': 'Type de Toilette '},
    color_discrete_sequence=px.colors.sequential.OrRd
)
pieType.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(pieType)

# st.write(filtered_data)

# Bar chart on statut
st.subheader("Disponibilités")
statut_group = filtered_data.groupby("STATUT").count()
bar = px.bar(statut_group,
             x=statut_group.index,
             y='TYPE',
             text='TYPE',
             labels={'TYPE': '', 'STATUT': ''}
             )
st.plotly_chart(bar)

# Bar chart on PMR
st.subheader("Accessibles pour les personnes à mobilité réduite")
acces_pmr = filtered_data.groupby("ACCES_PMR").count()
bar = px.bar(acces_pmr,
             x=acces_pmr.index,
             y='TYPE',
             text='TYPE',
             labels={'TYPE': '', 'ACCES_PMR': ''}
             )
st.plotly_chart(bar)

