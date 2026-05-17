#Rojas Rodríguez Alexis 6IV6

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Configuro la página de Streamlit para que se vea nice y no quede fea :3
st.set_page_config(page_title="Proyecto Estadistica", layout="wide")

# Título de la app :)
st.title("EXÁMEN PRÁCTICO 2DO PARCIAL - ROJAS RODRÍGUEZ ALEXIS")

# Explico de forma simple qué hace la app y por qué la armé así :D
st.write("""
Esta app carga un dataset con datos de peso, altura, velocidad y color.
El objetivo es mostrar la problemática con tablas, gráficas y cálculos estadísticos.

La página web la hice con Streamlit. Aunque no fue una herramienta
que vimos directamente en clase, investigué distintas opciones para
mostrar el análisis en una página web y Streamlit me pareció la más
sencilla de utilizar, además de que me permite usar Python y las
gráficas que vimos en clase.

Se incluyen:
- Frecuencia absoluta con gráfico de barras
- Frecuencia relativa con diagrama de pastel
- Frecuencia acumulada con gráfico de barras
- Polígono de frecuencias
- Media, mediana y moda
- Página web con información y gráficos usando Streamlit
""")

# Cargo los datos del archivo CSV con pandas
Datos = pd.read_csv("datos_examen.csv")

# Limpio las columnas numéricas para que queden bien y no rompan el cálculo
# to_numeric convierte texto a número y deja NaN en valores inválidos
for col in ["peso", "altura", "velocidad"]:
    if col in Datos.columns:
        Datos[col] = pd.to_numeric(Datos[col], errors="coerce")

# El color no es número, así que lo convierto a códigos para poder usarlo también
# Esto me deja tratar el color como dato cuantitativo cuando haga estadísticas
color_map = {"Blanco": 1, "Amarillo": 2, "Verde": 3}
if "color" in Datos.columns:
    Datos["color"] = Datos["color"].astype("category")
    Datos["color"] = Datos["color"].cat.set_categories(["Blanco", "Amarillo", "Verde"], ordered=True)
    Datos["color_codigo"] = pd.to_numeric(Datos["color"].map(color_map), errors="coerce")

# Muestro la tabla completa para que se pueda revisar todo fácil
st.header("TABLA DE DATOS")
st.dataframe(Datos)

# Calculo frecuencias para todas las columnas
# Uso esta lista para asegurarme de procesar solo las columnas que importan (en este caso son todas jaja)
columnas_freq = ["peso", "altura", "velocidad", "color"]
for col in columnas_freq:
    if col not in Datos.columns:
        continue

    st.subheader(f"Columna: {col}")

    # Frecuencia absoluta
    Frecuencia_Absoluta = Datos[col].value_counts().sort_index()
    st.write("Frecuencia absoluta:")
    st.write(Frecuencia_Absoluta)

    # Gráfico de barras para frecuencia absoluta.
    fig1, ax1 = plt.subplots(figsize=(7, 4))
    Frecuencia_Absoluta.plot(kind="bar", ax=ax1, color="tomato", edgecolor="black", linewidth=1.2)
    ax1.set_title(f"Frecuencia Absoluta - {col}", fontsize=14, fontweight="bold")
    ax1.set_xlabel(col, fontsize=12)
    ax1.set_ylabel("Cantidad", fontsize=12)
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(axis="y", alpha=0.3, linestyle="--")
    fig1.tight_layout()
    st.pyplot(fig1)
    plt.close(fig1)

    # Polígono de frecuencias
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    Frecuencia_Absoluta.plot(kind="line", marker="o", ax=ax2, color="turquoise", linewidth=2.5, markersize=8)
    ax2.set_title(f"Polígono de Frecuencias - {col}", fontsize=14, fontweight="bold")
    ax2.set_xlabel(col, fontsize=12)
    ax2.set_ylabel("Cantidad", fontsize=12)
    ax2.tick_params(axis='x', rotation=0)
    ax2.grid(alpha=0.3, linestyle="--")
    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

    # Frecuencia relativa
    Frecuencia_Relativa = Datos[col].value_counts(normalize=True).sort_index()
    st.write("Frecuencia relativa:")
    st.write(Frecuencia_Relativa)

    fig3, ax3 = plt.subplots(figsize=(7, 5))
    colors = ["tomato", "turquoise", "palegreen", "gold", "lightblue", "sandybrown"]
    Frecuencia_Relativa.plot(kind="pie", autopct="%1.1f%%", ax=ax3, colors=colors[:len(Frecuencia_Relativa)], 
                              textprops={"fontsize": 8})
    ax3.set_title(f"Frecuencia Relativa - {col}", fontsize=14, fontweight="bold")
    ax3.set_ylabel("")
    fig3.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)

    # Frecuencia acumulada
    Frecuencia_Acum = Frecuencia_Absoluta.cumsum()
    st.write("Frecuencia acumulada:")
    st.write(Frecuencia_Acum)

    fig4, ax4 = plt.subplots(figsize=(7, 4))
    Frecuencia_Acum.plot(kind="bar", ax=ax4, color="turquoise", edgecolor="black", linewidth=1.2)
    ax4.set_title(f"Frecuencia Acumulada - {col}", fontsize=14, fontweight="bold")
    ax4.set_xlabel(col, fontsize=12)
    ax4.set_ylabel("Cantidad", fontsize=12)
    ax4.tick_params(axis='x', rotation=45)
    ax4.grid(axis="y", alpha=0.3, linestyle="--")
    fig4.tight_layout()
    st.pyplot(fig4)
    plt.close(fig4)

# Calculo estadísticas básicas para cada columna numérica disponible
st.header("MEDIA, MEDIANA Y MODA")
num_cols = Datos.select_dtypes(include=["number"]).columns.tolist()
if len(num_cols) == 0:
    st.write("No hay columnas numéricas para calcular estadísticas :(")
else:
    for col in num_cols:
        # Calculamos las medidas centrales para la cada columna
        media = Datos[col].mean()
        mediana = Datos[col].median()
        moda = Datos[col].mode()

        label = "color (codificado)" if col == "color_codigo" else col
        st.write(f"**Columna:** {label}")
        st.write(f"- Media: {round(media, 2)}")
        st.write(f"- Mediana: {round(mediana, 2)}")
        if not moda.empty:
            st.write(f"- Moda: {list(moda)}")
        else:
            st.write("- Moda: No hay moda definida :(")
        st.write("")

# Mensaje final que dice que todo cargó bien y se ejecutó sin errores
st.success("Ejecutado correctamente")
