
import streamlit as st
import pandas as pd

# Título de la página
st.title("📊 Comparar horarios")

# Comprobar si existen datos cargados
if "datos" not in st.session_state:

    st.warning("Primero debes cargar los datos en Explorar los datos.")

else:

    # Recuperar los datos
    df = st.session_state["datos"]

    # --------------------------------
    # Filtros compartidos
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

    # Seleccionar columna según usuario
    if usuario == "Ocasionales":
        columna = "alquileres_ocasionales"

    elif usuario == "Registrados":
        columna = "alquileres_registrados"

    else:
        columna = "alquileres_total"

    # Crear columna de alquileres seleccionados
    datos_filtrados["alquileres"] = datos_filtrados[columna]

    # --------------------------------
    # R6: Promedio por hora
    # --------------------------------

    st.subheader("Promedio de alquileres por hora")

    # Agrupar por hora y calcular promedio
    promedio_horas = datos_filtrados.groupby(
        "hora"
    )["alquileres"].mean().reset_index()

    promedio_horas = promedio_horas.rename(
        columns={"alquileres": "promedio"}
    )

    # Selector de color
    color_barras = st.color_picker(
        "Selecciona el color de las barras",
        "#1f77b4"
    )

    # Crear gráfico de barras
    st.bar_chart(
        promedio_horas,
        x="hora",
        y="promedio",
        color=color_barras,
        x_label="Hora del día",
        y_label="Promedio de alquileres"
    )

    # Casilla para mostrar tabla
    mostrar_tabla = st.checkbox(
        "Mostrar tabla de promedios"
    )

    if mostrar_tabla:

        st.dataframe(
            promedio_horas,
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------
    # R7: Comparar con un límite
    # --------------------------------

    st.subheader("Comparación con límite de alquileres")

    limite = st.number_input(
        "Límite de alquileres por hora",
        min_value=0,
        value=250,
        step=50
    )

    # Identificar horas que superan el límite
    horas_superiores = promedio_horas[
        promedio_horas["promedio"] > limite
    ]

    # Mostrar cantidad de horas
    cantidad = len(horas_superiores)
    total_horas = len(promedio_horas)

    st.metric(
        "Horas que superan el límite",
        f"{cantidad} de {total_horas}"
    )

    # Mostrar horarios encontrados
    if cantidad > 0:

        st.write("Horarios que superan el límite:")

        st.dataframe(
            horas_superiores,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Ninguna hora supera el límite seleccionado.")

