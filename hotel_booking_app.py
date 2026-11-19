########################################################
##################### LIBRERÍAS ########################
########################################################

import streamlit as st
import pandas as pd
import plotly.express as px

########################################################
################ CONFIGURACIÓN APP #####################
########################################################

st.set_page_config(
    page_title="Hotel Booking Analytics",
    page_icon="🏨",
    layout="wide"
)

########################################################
################ CARGAR DATASET ########################
########################################################

@st.cache_data
def load_data():

    df = pd.read_csv(
        "hotel_bookings_clean.csv"
    )

    return df


df = load_data()

########################################################
############ ORDENAR MESES CORRECTAMENTE ###############
########################################################

month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

df["arrival_date_month"] = pd.Categorical(
    df["arrival_date_month"],
    categories=month_order,
    ordered=True
)

########################################################
##################### SIDEBAR ##########################
########################################################

st.sidebar.title("🏨 Hotel Booking Analytics")

pagina = st.sidebar.radio(
    "Seleccione una sección",
    [
        "🏠 Inicio",
        "📊 Demanda de Reservas",
        "❌ Cancelaciones",
        "💰 ADR y Precios",
        "🌎 Mercado y Clientes",
        "📂 Dataset"
    ]
)

########################################################
##################### INICIO ###########################
########################################################

if pagina == "🏠 Inicio":

    st.title("🏨 Hotel Booking Analytics Dashboard")

    st.markdown("""
    ### Proyecto de Analítica de Datos Hoteleros

    Dashboard desarrollado como complemento del proyecto de análisis de reservas hoteleras.

    **Herramientas utilizadas**

    - Python
    - SQL (MariaDB)
    - R
    - Streamlit
    - Plotly

    **Objetivos**

    - Analizar la demanda de reservas.
    - Identificar factores asociados a las cancelaciones.
    - Estudiar el comportamiento del ADR.
    - Evaluar segmentos de mercado.
    - Analizar países de origen.
    - Encontrar patrones de negocio.
    """)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Reservas",
        f"{len(df):,}"
    )

    col2.metric(
        "Hoteles",
        df["hotel"].nunique()
    )

    col3.metric(
        "Países",
        df["country"].nunique()
    )

    col4.metric(
        "ADR Promedio",
        round(
            df["adr"].mean(),
            2
        )
    )

    st.divider()

    st.success(
        """
        Principales hallazgos

        ✅ El City Hotel concentra la mayor demanda.

        ✅ Las reservas más anticipadas presentan mayor probabilidad de cancelación.

        ✅ El Resort Hotel posee tarifas promedio más elevadas.

        ✅ Online TA es el principal segmento de mercado.

        ✅ Las solicitudes especiales reducen la tasa de cancelación.
        """
    )

########################################################
############### DEMANDA DE RESERVAS ####################
########################################################

elif pagina == "📊 Demanda de Reservas":

    st.title("📊 Demanda de Reservas")

    demanda_df = (
        df.groupby(
            [
                "hotel",
                "arrival_date_year",
                "arrival_date_month"
            ],
            observed=True
        )
        .size()
        .reset_index(
            name="total_reservas"
        )
    )

    fig = px.bar(
        demanda_df,
        x="arrival_date_month",
        y="total_reservas",
        color="hotel",
        facet_col="arrival_date_year",
        barmode="group",
        title="Demanda de reservas por hotel y período"
    )

    fig.update_layout(
        height=600
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "El City Hotel presenta el mayor volumen de reservas durante gran parte del período analizado."
    )

########################################################
################### CANCELACIONES ######################
########################################################

elif pagina == "❌ Cancelaciones":

    st.title("❌ Anticipación y Cancelaciones")

    cancelacion_df = (
        df.groupby(
            "is_canceled"
        )["lead_time"]
        .mean()
        .reset_index()
    )

    cancelacion_df["Estado"] = (
        cancelacion_df["is_canceled"]
        .replace(
            {
                0: "No cancelada",
                1: "Cancelada"
            }
        )
    )

    fig = px.bar(
        cancelacion_df,
        x="Estado",
        y="lead_time",
        color="Estado",
        text_auto=".2f",
        title="Anticipación promedio según estado de reserva"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.warning(
        "Las reservas canceladas presentan una anticipación promedio significativamente mayor."
    )

########################################################
################### ADR Y PRECIOS ######################
########################################################

elif pagina == "💰 ADR y Precios":

    st.title("💰 Comportamiento del ADR")

    adr_df = (
        df.groupby(
            [
                "hotel",
                "arrival_date_year",
                "arrival_date_month"
            ],
            observed=True
        )["adr"]
        .mean()
        .reset_index()
    )

    year = st.selectbox(
        "Seleccione el año",
        sorted(
            adr_df["arrival_date_year"]
            .unique()
        )
    )

    adr_filtered = (
        adr_df[
            adr_df["arrival_date_year"] == year
        ]
    )

    fig = px.line(
        adr_filtered,
        x="arrival_date_month",
        y="adr",
        color="hotel",
        markers=True,
        title=f"ADR promedio durante {year}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "El Resort Hotel presenta mayor volatilidad y niveles de ADR superiores al City Hotel."
    )

########################################################
############### MERCADO Y CLIENTES #####################
########################################################

elif pagina == "🌎 Mercado y Clientes":

    st.title("🌎 Mercado y Clientes")

    tab1, tab2, tab3 = st.tabs(
        [
            "Segmentos",
            "Países",
            "Solicitudes Especiales"
        ]
    )

########################################################
###################### SEGMENTOS #######################
########################################################

    with tab1:

        segmento_df = (
            df.groupby(
                "market_segment"
            )
            .size()
            .reset_index(
                name="reservas"
            )
            .sort_values(
                "reservas",
                ascending=False
            )
        )

        fig = px.bar(
            segmento_df,
            x="market_segment",
            y="reservas",
            color="market_segment",
            title="Reservas por segmento de mercado"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

########################################################
######################## PAÍSES ########################
########################################################

    with tab2:

        paises_df = (
            df.groupby(
                "country"
            )
            .size()
            .reset_index(
                name="reservas"
            )
            .sort_values(
                "reservas",
                ascending=False
            )
            .head(10)
        )

        fig = px.bar(
            paises_df,
            x="country",
            y="reservas",
            color="reservas",
            title="Top 10 países por número de reservas"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

########################################################
############### SOLICITUDES ESPECIALES #################
########################################################

    with tab3:

        solicitudes_df = (
            df.groupby(
                "total_of_special_requests"
            )["is_canceled"]
            .mean()
            .reset_index()
        )

        solicitudes_df[
            "tasa_cancelacion"
        ] = (
            solicitudes_df[
                "is_canceled"
            ] * 100
        )

        fig = px.scatter(
            solicitudes_df,
            x="total_of_special_requests",
            y="tasa_cancelacion",
            size="tasa_cancelacion",
            trendline="ols",
            title="Solicitudes especiales vs tasa de cancelación"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.success(
            "Existe una relación inversa entre la cantidad de solicitudes especiales y la tasa de cancelación."
        )

########################################################
###################### DATASET #########################
########################################################

elif pagina == "📂 Dataset":

    st.title("📂 Dataset")

    filas = st.slider(
        "Número de registros a visualizar",
        5,
        100,
        20
    )

    st.dataframe(
        df.head(filas),
        use_container_width=True
    )

    st.write(
        f"Total de registros: {len(df):,}"
    )

    st.write(
        f"Total de columnas: {len(df.columns)}"
    )