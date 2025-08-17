import os
import pandas as pd
import streamlit as st
from datetime import datetime

DATA_DIR = "datos_sinteticos"
CSV_PATH = os.path.join(DATA_DIR, "products.csv")

ALLOWED_CATEGORIES = [
    "Chocolates", "Caramelos", "Mashmelos", "Galletas", "Salados", "Gomas de mascar"
]

def ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def load_df() -> pd.DataFrame:
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH, encoding="utf-8")
        return df
    return pd.DataFrame(columns=["nombre", "precio", "categorias", "en_venta", "ts"])

def validate(nombre: str, precio, categorias: list, en_venta_label: str):
    #nombre
    if len(nombre.strip()) == 0 or len(nombre.strip()) > 20:
        raise ValueError("El nombre no puede estar vacío ni superar 20 caracteres.")
    
    #precio
    if precio is None:
        raise ValueError("Por favor verifique el campo del precio")
    try:
        p = float(precio)
    except Exception:
        raise ValueError("Por favor verifique el campo precio")
    if not (0 < p < 999):
        raise ValueError("El precio debe ser mayor a 0 y menor a 999.")
    
    #categorias
    if not categorias:
        raise ValueError("Debe elegir al menos una categoría.")
    for c in categorias:
        if c not in ALLOWED_CATEGORIES:
            raise ValueError(f"Categoría inválida: {c}")
    #en venta
    if en_venta_label not in ["Sí", "No"]:
        raise ValueError("Valor inválido para ¿está en venta?")
    return nombre.strip(), round(p,2), sorted(list(set(categorias))), (en_venta_label == "Sí")


#------------------------------------- UI -----------------------------------

st.title("Confitería Dulcino - Registro de productos")

with st.form("form-producto", clear_on_submit=True):
    col1, col2 = st.columns([2,1])
    with col1:
        nombre = st.text_input("Nombre del producto")
    with col2:
        precio = st.number_input("Precio (S/)", min_value=0.0, max_value=998.99, step=0.10, format="%.2f")
    categorias = st.multiselect("Categorias", ALLOWED_CATEGORIES)
    en_venta_label = st.radio("¿El producto está en venta?", options=["Sí", "No"], horizontal=True)

    submitted = st.form_submit_button("Guardar")

if submitted:
    try:
        ensure_dir()
        nombre_val, precio_val, categorias_val, en_venta_val = validate(
            nombre, precio, categorias, en_venta_label
        )

        df = load_df()
        nuevo = {
            "nombre": nombre_val,
            "precio": precio_val,
            "categorias": ";".join(categorias_val),  # se guarda como string
            "en_venta": en_venta_val,
            "ts": datetime.now().isoformat()
        }

        df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
        df.to_csv(CSV_PATH, index=False, encoding="utf-8")

        st.success("✅ Producto guardado correctamente")

    except ValueError as e:
        st.error(f"⚠️ Error de validación: {e}")

    except Exception as e:
        st.error(f"❌ Error inesperado: {e}")