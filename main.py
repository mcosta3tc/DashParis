import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk


def openHours(hours):
    if hours[0] != "":
        if hours[0] == "24" and hours[1] == "24":
            return 24
        else:
            return int(hours[1]) - (int(hours[0]))


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
    toilettes["Open Hours"] = toilettes.HORAIRE.str.replace("\D+", "&").fillna("").apply(lambda x: x.split("&")).apply(
        openHours)
    return toilettes


# General dataset
data = get_data()
# Filtered dataset
filtered_data = ""


# Display a header
def header():
    st.title("Les toilettes publiques à Paris")
    # Add spacing
    st.markdown("""#""")


# Display a map
def map_frame(data_set, zoom, location):
    if location == "sidebar":
        st.sidebar.map(
            data_set,
            zoom=zoom
        )
    elif location == "page":
        st.map(
            data_set,
            zoom=zoom
        )


# Display a Pie chart
def pie_frame(data_set):
    pie_type = px.pie(
        data_set,
        values='arr',
        names='TYPE',
        hover_data=['arr'],
        labels={'arr': 'Arrondissement ', 'TYPE': 'Type de Toilette '},
        color_discrete_sequence=px.colors.sequential.OrRd
    )
    pie_type.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(pie_type)


def bar_chart_grouped_frame(data_set, group, header_title):
    st.subheader(header_title)
    grouped = data_set.groupby(str(group)).count()
    bar_frame = px.bar(
        grouped,
        x=grouped.index,
        y='TYPE',
        text='TYPE',
        labels={'TYPE': '', str(group): ''},
    )
    bar_frame.update_layout(
        yaxis=dict(
            title='Nbr de disponibilité'
        )
    )
    st.plotly_chart(bar_frame)


# SIDEBAR
st.sidebar.title("Choisir un mode")
st.sidebar.write("Affichez des information en rapport avec Paris ou votre arrondissement")
# Dropdown
sidebar_option = st.sidebar.selectbox("", ('Paris', 'Arrondissement'))

# SHOW CONTENT
if sidebar_option == 'Arrondissement':
    # Display header
    header()

    # Sidebar header
    st.sidebar.title("Choisir un arrondissement")
    arr_to_filter = st.sidebar.slider('Du 1er au 20e arrondissement de Paris', 1, 20, 5)
    st.sidebar.write("Vous êtes dans le ", arr_to_filter, "arrondissement de Paris")
    # filter data
    filtered_data = data[data['arr'] == arr_to_filter]
    # Display filtered map in the sidebar
    map_frame(filtered_data, 11.3, "sidebar")

    st.subheader("Type de toilettes dans le " + str(arr_to_filter) + "e arrondissement")
    # Pie chart types of toilettes by arrondissement
    pie_frame(filtered_data)

    # Bar chart on statut
    bar_chart_grouped_frame(filtered_data, "STATUT", "Disponibilités")

    # Bar chart on PMR
    bar_chart_grouped_frame(filtered_data, "ACCES_PMR", "Accessibles pour les personnes à mobilité réduite")

    st.write(filtered_data)


elif sidebar_option == 'Paris':
    # Display header
    header()

    # Sidebar
    # count of toilets
    total = data.count().TYPE
    st.sidebar.write("Actuellement il y a plus de ", total, " toilettes publiques dans Paris :toilet:")
    st.sidebar.write("Elles sont ouvertes en moyenne ")
    st.sidebar.write(round(data['Open Hours'].mean()), "h sur 24")

    # Page
    # general map of toilets in Paris
    map_frame(data, 11, "page")

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

    st.subheader("Type de toilettes dans Paris")
    # Pie chart types of toilettes
    pie_frame(data)

    # Bar chart on statut
    bar_chart_grouped_frame(data, "STATUT", "Disponibilités")

    # Bar chart on PMR
    bar_chart_grouped_frame(data, "ACCES_PMR", "Accessibles pour les personnes à mobilité réduite")

    st.plotly_chart(px.line(data, x="arr", y="Open Hours"))

    st.write(data)
