import streamlit as st
import requests
import re

# CONFIG
SUPABASE_URL = "https://uewjwciwyhwlqnuucjkc.supabase.co"
SUPABASE_KEY = "sb_publishable_er7GMgAwXRRyVf8nHupxAQ_IWtWG2an"
TELEGRAM_TOKEN = "8701147786:AAEUmLT-UMZAlS-GvvizXeeyj0vs2a-z6SA"
CHAT_ID = "8698188310"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

st.set_page_config(page_title="SÍ AL MÉRITO", layout="wide")

# TELEGRAM
def enviar_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except:
        pass

# SESSION
if "user" not in st.session_state:
    st.session_state.user = None

# REGISTRO
if st.session_state.user is None:

    st.title("SÍ AL MÉRITO")
    st.subheader("Registro")

    nombre = st.text_input("Nombre", key="n")
    cedula = st.text_input("Cédula", key="c")
    correo = st.text_input("Correo", key="e")
    celular = st.text_input("Celular", key="t")

    if st.button("Registrarse"):

        if not (nombre and cedula and correo and celular):
            st.error("Completa todo")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            st.error("Correo inválido")
        else:
            url = f"{SUPABASE_URL}/rest/v1/Usuarios"

            data = {
                "Nombre": nombre,
                "Cedula": cedula,
                "Correo": correo,
                "Celular": celular
            }

            r = requests.post(url, json=data, headers=headers)

            if r.status_code == 201:
                st.session_state.user = nombre
                enviar_telegram(f"Nuevo registro: {nombre}")
                st.success("OK")
                st.rerun()
            else:
                st.error(r.text)

else:
    st.success(f"Bienvenido {st.session_state.user}")
