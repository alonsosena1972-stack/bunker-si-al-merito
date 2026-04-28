

import streamlit as st
import requests
import re

# ===============================
# 🔑 CONFIGURACIÓN
# ===============================
SUPABASE_URL = "https://uewjwciwyhwlqnuucjkc.supabase.co"
SUPABASE_KEY = "sb_publishable_er7GMgAwXRRyVf8nHupxAQ_IWtWG2an"

TELEGRAM_TOKEN = "8701147786:AAEUmLT-UMZAlS-GvvizXeeyj0vs2a-z6SA"
CHAT_ID = "8698188310"

ADMIN_PASSWORD = "merito2026"
WHATSAPP_NUMERO = "573146715497"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

st.set_page_config(page_title="SÍ AL MÉRITO", layout="wide")

# ===============================
# 🔔 TELEGRAM
# ===============================
def enviar_telegram(mensaje):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": mensaje})
    except:
        pass

# ===============================
# 🎨 HEADER
# ===============================
st.image("logo.jpg", width=120)
st.title("SÍ AL MÉRITO")
st.info("Accede a noticias, comunidad y asesoría para concursos públicos")

# ===============================
# 🔐 SESSION
# ===============================
if "user" not in st.session_state:
    st.session_state.user = None

if "admin" not in st.session_state:
    st.session_state.admin = False

# ===============================
# VALIDACIONES
# ===============================
def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validar_cedula(c):
    return c.isdigit()

def validar_celular(c):
    return c.isdigit()

# ===============================
# 🔐 REGISTRO
# ===============================
if st.session_state.user is None:

    st.subheader("Registro de usuarios")

    nombre = st.text_input("Nombre", key="nombre")
    cedula = st.text_input("Cédula", key="cedula")
    correo = st.text_input("Correo", key="correo")
    celular = st.text_input("Celular", key="celular")

    if st.button("Registrarse"):

        if not (nombre and cedula and correo and celular):
            st.error("Completa todos los campos")

        elif not validar_email(correo):
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
                st.success("Registro exitoso")

                enviar_telegram(
                    f"🚨 Nuevo registro\n{nombre}\n{correo}\n{celular}"
                )

                st.rerun()
            else:
                st.error(r.text)

# ===============================
# 🧠 SISTEMA PRINCIPAL
# ===============================
else:

    st.success(f"Bienvenido {st.session_state.user}")

    # SIDEBAR
    st.sidebar.markdown(f"👤 {st.session_state.user}")

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.user = None
        st.session_state.admin = False
        st.rerun()

    # ADMIN
    clave = st.sidebar.text_input("Clave admin", type="password")

    if clave == ADMIN_PASSWORD:
        st.session_state.admin = True
        st.sidebar.success("Admin activo")

    # PUBLICAR NOTICIA
    if st.session_state.admin:
        st.sidebar.subheader("Publicar noticia")

        titulo = st.sidebar.text_input("Título")
        contenido = st.sidebar.text_area("Contenido")

        if st.sidebar.button("Publicar"):

            url = f"{SUPABASE_URL}/rest/v1/noticias"

            data = {
                "titulo": titulo,
                "contenido": contenido,
                "autor": st.session_state.user
            }

            requests.post(url, json=data, headers=headers)
            st.sidebar.success("Publicada")

    # WHATSAPP
    link_wp = f"https://wa.me/{WHATSAPP_NUMERO}?text=Hola%20quiero%20información"
    st.markdown(f"[💬 WhatsApp]({link_wp})")

    st.markdown("---")

    # NOTICIAS
    st.subheader("Noticias")

    url = f"{SUPABASE_URL}/rest/v1/noticias?select=*"
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        for n in r.json():
            st.write(f"### {n['titulo']}")
            st.write(n["contenido"])
            st.write("---")

    # CHAT
    st.subheader("Comunidad")

    mensaje = st.text_input("Mensaje", key="mensaje")

    if st.button("Enviar"):

        url = f"{SUPABASE_URL}/rest/v1/mensajes"

        data = {
            "usuario": st.session_state.user,
            "mensaje": mensaje
        }

        requests.post(url, json=data, headers=headers)
        enviar_telegram(f"{st.session_state.user}: {mensaje}")
        st.rerun()

    # VER MENSAJES
    url = f"{SUPABASE_URL}/rest/v1/mensajes?select=*"
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        for m in r.json():
            st.write(f"{m['usuario']}: {m['mensaje']}")

    # IA
    st.subheader("Asistente")

    pregunta = st.text_input("Pregunta", key="pregunta")

    if st.button("Consultar"):
        st.info("Estudia normativa y práctica constante.")
# version nueva
