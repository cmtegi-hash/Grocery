"""
Lista de mercado — App de la PC
Aquí administras el catálogo (todo lo que sueles comprar) y la lista
activa (lo que hace falta ahora). El botón "Sincronizar" sube el
archivo JSON a GitHub para que el iPhone lo pueda leer.
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

import streamlit as st

DATA_PATH = Path(__file__).parent / "data" / "lista_mercado.json"

st.set_page_config(page_title="Lista de mercado", page_icon="🛒", layout="centered")


# --- Utilidades de datos -----------------------------------------------

def cargar_datos():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_datos(datos):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def existe_en_catalogo(catalogo, nombre):
    """Compara sin importar mayúsculas/minúsculas."""
    nombre_normalizado = nombre.strip().lower()
    return any(item.strip().lower() == nombre_normalizado for item in catalogo)


def existe_en_lista_activa(lista_activa, nombre):
    nombre_normalizado = nombre.strip().lower()
    return any(item.strip().lower() == nombre_normalizado for item in lista_activa)


if "datos" not in st.session_state:
    st.session_state.datos = cargar_datos()

datos = st.session_state.datos


# --- Encabezado ----------------------------------------------------------

st.title("🛒 Lista de mercado")

ultima = datos.get("ultima_sincronizacion")
if ultima:
    st.caption(f"Última sincronización: {ultima}")
else:
    st.caption("Todavía no se ha sincronizado")


# --- Agregar ítem nuevo ---------------------------------------------------

st.subheader("Agregar algo nuevo")

with st.form("form_agregar", clear_on_submit=True):
    nuevo_item = st.text_input("Nombre del ítem", placeholder="Ej. Detergente")
    enviado = st.form_submit_button("Agregar")

    if enviado:
        nuevo_item = nuevo_item.strip()
        if not nuevo_item:
            st.warning("Escribe un nombre antes de agregar.")
        elif existe_en_catalogo(datos["catalogo"], nuevo_item):
            st.warning(f'"{nuevo_item}" ya existe en el catálogo. Selecciónalo abajo en vez de agregarlo de nuevo.')
        else:
            datos["catalogo"].append(nuevo_item)
            datos["lista_activa"].append(nuevo_item)
            guardar_datos(datos)
            st.success(f'"{nuevo_item}" agregado al catálogo y a la lista activa.')
            st.rerun()


# --- Catálogo --------------------------------------------------------------

st.subheader("Catálogo (todo lo que sueles comprar)")

if not datos["catalogo"]:
    st.info("Todavía no hay ítems en el catálogo. Agrega el primero arriba.")
else:
    for item in sorted(datos["catalogo"], key=str.lower):
        col1, col2, col3 = st.columns([3, 2, 1])
        col1.write(item)

        ya_en_lista = existe_en_lista_activa(datos["lista_activa"], item)
        if col2.button(
            "En lista ✓" if ya_en_lista else "+ Agregar a lista",
            key=f"add_{item}",
            disabled=ya_en_lista,
        ):
            datos["lista_activa"].append(item)
            guardar_datos(datos)
            st.rerun()

        if col3.button("🗑", key=f"del_cat_{item}", help="Eliminar del catálogo"):
            st.session_state[f"confirmar_{item}"] = True

        if st.session_state.get(f"confirmar_{item}"):
            st.warning(f'¿Eliminar "{item}" del catálogo para siempre?')
            c1, c2 = st.columns(2)
            if c1.button("Sí, eliminar", key=f"si_{item}"):
                datos["catalogo"] = [i for i in datos["catalogo"] if i != item]
                datos["lista_activa"] = [i for i in datos["lista_activa"] if i != item]
                guardar_datos(datos)
                del st.session_state[f"confirmar_{item}"]
                st.rerun()
            if c2.button("Cancelar", key=f"no_{item}"):
                del st.session_state[f"confirmar_{item}"]
                st.rerun()


# --- Lista activa ------------------------------------------------------------

st.subheader("Lista activa (pendiente de comprar)")

if not datos["lista_activa"]:
    st.info("No hay nada pendiente. Agrega algo nuevo o selecciónalo del catálogo.")
else:
    for item in datos["lista_activa"]:
        col1, col2 = st.columns([4, 1])
        col1.write(item)
        if col2.button("Quitar", key=f"quitar_{item}"):
            datos["lista_activa"] = [i for i in datos["lista_activa"] if i != item]
            guardar_datos(datos)
            st.rerun()


# --- Sincronizar con GitHub -----------------------------------------------

st.divider()

if st.button("🔄 Sincronizar al iPhone", type="primary"):
    ahora = datetime.now().strftime("%d %b, %I:%M %p")
    datos["ultima_sincronizacion"] = ahora
    guardar_datos(datos)

    try:
        repo_dir = Path(__file__).parent
        subprocess.run(["git", "add", "data/lista_mercado.json"], cwd=repo_dir, check=True)
        subprocess.run(
            ["git", "commit", "-m", f"Sincronizar lista - {ahora}"],
            cwd=repo_dir,
            check=True,
        )
        subprocess.run(["git", "push"], cwd=repo_dir, check=True)
        st.success(f"Sincronizado correctamente a las {ahora}.")
        st.rerun()
    except subprocess.CalledProcessError as e:
        st.error(
            "No se pudo subir a GitHub automáticamente. "
            "Puedes subirlo tú mismo con git add / commit / push.\n\n"
            f"Detalle: {e}"
        )
