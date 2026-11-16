
import streamlit as st
import pandas as pd

# Título de la página
st.title("🚲 Explorar los datos")

# --------------------------------
# R1: Cargar los datos
# --------------------------------

st.subheader("Carga de datos")

archivo = st.file_uploader(
    "Selecciona el archivo CSV",
    type=["csv"]
)

if st.button("Cargar datos"):

    if archivo is not None:

        # Leer el archivo CSV
        df = pd.read_csv(
            archivo,
            encoding="utf-8-sig",
            parse_dates=["fecha"]
        )

        # Guardar los datos
        st.session_state["datos"] = df

        st.success(
            f"Se cargaron {len(df)} registros correctamente."
        )

    else:
        st.warning("Primero debes seleccionar el archivo CSV.")

# --------------------------------
# Comprobar si existen datos
# --------------------------------

if "datos" not in st.session_state:

    st.info("Para comenzar, selecciona y carga el archivo CSV.")

else:

    df = st.session_state["datos"]

    # --------------------------------
    # R3: Filtros compartidos
    # --------------------------------

    st.sidebar.header("Filtros")

    usuario = st.sidebar.selectbox(
        "Tipo de usuario",
        ["Todos", "Ocasionales", "Registrados"],
        key="usuario"
    )

    tipo_dia = st.sidebar.radio(
        "Tipo de día",
        ["Todos", "Laborable", "No laborable"],
        key="tipo_dia"
    )

    horas = st.sidebar.slider(
        "Horas del día",
        min_value=0,
        max_value=23,
        value=(0, 23),
        key="horas"
    )

    # Aplicar filtros
    datos_filtrados = df.copy()

    if tipo_dia != "Todos":
        datos_filtrados = datos_filtrados[
            datos_filtrados["tipo_dia"] == tipo_dia
        ]

    datos_filtrados = datos_filtrados[
        (datos_filtrados["hora"] >= horas[0]) &
        (datos_filtrados["hora"] <= horas[1])
    ]

    # Seleccionar tipo de alquiler
    if usuario == "Ocasionales":
        columna = "alquileres_ocasionales"

    elif usuario == "Registrados":
        columna = "alquileres_registrados"

    else:
        columna = "alquileres_total"

    # Guardar selección y datos filtrados
    st.session_state["columna"] = columna
    st.session_state["datos_filtrados"] = datos_filtrados

    # --------------------------------
    # R2: Crear pestañas
    # --------------------------------

    tab1, tab2 = st.tabs(["Gráfico diario", "Datos"])

    with tab1:
        st.subheader("Gráfico diario")

        st.info("Aquí construiremos el gráfico de alquileres diarios.")

    with tab2:
        st.subheader("Datos")

        st.info("Aquí construiremos la tabla y descarga CSV.")

