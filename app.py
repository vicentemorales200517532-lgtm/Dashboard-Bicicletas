
import streamlit as st

# Configuración de la aplicación
st.set_page_config(
    page_title="Dashboard Bicicletas",
    page_icon="🚲",
    layout="wide"
)

# Crear las páginas
pagina1 = st.Page(
    "pages/1_Explorar_datos.py",
    title="Explorar los datos",
    default=True
)

pagina2 = st.Page(
    "pages/2_Comparar_horarios.py",
    title="Comparar horarios"
)

# Configurar la navegación
pagina = st.navigation([pagina1, pagina2])

# Ejecutar la página seleccionada
pagina.run()
