
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

  
# --------------------------------
# R4: Indicadores
# --------------------------------

# Crear una columna con el tipo de alquiler seleccionado
datos_filtrados = datos_filtrados.copy()
datos_filtrados["alquileres"] = datos_filtrados[columna]

# Calcular indicadores
total_alquileres = datos_filtrados["alquileres"].sum()
promedio_alquileres = datos_filtrados["alquileres"].mean()

# Mostrar indicadores
st.subheader("Indicadores generales")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total de alquileres",
        f"{total_alquileres:,.0f}"
    )

with col2:
    st.metric(
        "Promedio por hora observada",
        f"{promedio_alquileres:.1f}"
    )

# --------------------------------
# R2: Crear pestañas
# --------------------------------


# --------------------------------
# R4: Indicadores
# --------------------------------

# Crear una columna con el tipo de alquiler seleccionado
datos_filtrados = datos_filtrados.copy()
datos_filtrados["alquileres"] = datos_filtrados[columna]

# Calcular indicadores
total_alquileres = datos_filtrados["alquileres"].sum()
promedio_alquileres = datos_filtrados["alquileres"].mean()

# Mostrar indicadores
st.subheader("Indicadores generales")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total de alquileres",
        f"{total_alquileres:,.0f}"
    )

with col2:
    st.metric(
        "Promedio por hora observada",
        f"{promedio_alquileres:.1f}"
    )

# --------------------------------
# R2: Crear pestañas
# --------------------------------

tab1, tab2 = st.tabs(["Gráfico diario", "Datos"])

with tab1:

    st.subheader("Alquileres diarios")

    # Agrupar los alquileres por fecha
    grafico_diario = datos_filtrados.groupby(
        "fecha"
    )["alquileres"].sum().reset_index()

    # Ordenar por fecha
    grafico_diario = grafico_diario.sort_values("fecha")

    # Crear gráfico de líneas
    st.line_chart(
        grafico_diario,
        x="fecha",
        y="alquileres",
        x_label="Fecha",
        y_label="Total de alquileres"
    )


with tab2:

    st.subheader("Datos de alquileres")

    # Mostrar tabla interactiva
    st.dataframe(
        datos_filtrados,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------
    # Descargar datos filtrados
    # --------------------------------

    # Convertir los datos a formato CSV
    csv = datos_filtrados.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="Descargar datos CSV",
        data=csv,
        file_name="bicicletas_filtradas.csv",
        mime="text/csv"
    )

    # --------------------------------
    # Fuente de los datos
    # --------------------------------

    st.subheader("Fuente de los datos")

    st.write(
        "Fanaee-T, H. (2013). Bike Sharing "
        "[Conjunto de datos]. UCI Machine Learning Repository."
    )

    st.write("DOI: 10.24432/C5W894. Licencia CC BY 4.0.")

    st.link_button(
        "Consultar fuente UCI",
        "https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset"
    )
