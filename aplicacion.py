import streamlit as st
from datetime import datetime
import os
from PIL import Image

# --- CONFIGURACIÓN Y ESTILOS ---
st.set_page_config(page_title="SÍ AL MÉRITO - Búnker", page_icon="🚀", layout="wide")

# COLOR VERDE CORPORATIVO: #28a745 (Verde éxito)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { border-radius: 20px; width: 100%; font-weight: bold; }
    .titulo-verde { color: #28a745; font-weight: bold; }
    .noticia-box {
        background-color: #1E1E1E;
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #28a745;
        color: white;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ARCHIVOS DE BASE DE DATOS ---
ARCHIVO_CHAT = "base_datos_chat.txt"
ARCHIVO_NOTICIA = "ultima_noticia.txt"
ARCHIVO_USUARIOS = "usuarios_registrados.txt"

# --- FUNCIONES DE MEMORIA (Se mantienen igual) ---
def guardar_usuario(nombre, cedula, correo, celular):
    with open(ARCHIVO_USUARIOS, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()}|{nombre}|{cedula}|{correo}|{celular}\n")

def guardar_mensaje(usuario, texto):
    fecha = datetime.now().strftime("%d/%m %H:%M")
    with open(ARCHIVO_CHAT, "a", encoding="utf-8") as f:
        f.write(f"{fecha}|{usuario}|{texto}\n")

def cargar_mensajes():
    mensajes = []
    if os.path.exists(ARCHIVO_CHAT):
        with open(ARCHIVO_CHAT, "r", encoding="utf-8") as f:
            for linea in f:
                p = linea.strip().split("|")
                if len(p) == 3: mensajes.append({"fecha": p[0], "usuario": p[1], "texto": p[2]})
    return mensajes

def guardar_noticia(titulo, contenido, autor):
    with open(ARCHIVO_NOTICIA, "w", encoding="utf-8") as f:
        f.write(f"{titulo}|{contenido}|{autor}")

def cargar_noticia():
    if os.path.exists(ARCHIVO_NOTICIA):
        with open(ARCHIVO_NOTICIA, "r", encoding="utf-8") as f:
            p = f.read().split("|")
            if len(p) == 3: return {"titulo": p[0], "contenido": p[1], "autor": p[2]}
    return {"titulo": "PROCESOS DE MÉRITO EN COLOMBIA", "contenido": "Aún no hay noticias publicadas.", "autor": "César Padilla"}

# --- LÓGICA DE ACCESO ---
if "autenticado" not in st.session_state:
    # Mostramos el nombre de la empresa en VERDE en el registro
    st.markdown("<h1 style='text-align: center;' class='titulo-verde'>SÍ AL MÉRITO</h1>", unsafe_allow_html=True)
    st.info("Para ingresar al Búnker, por favor registre sus datos.")
    
    with st.form("registro"):
        c1, c2 = st.columns(2)
        with c1:
            nom = st.text_input("Nombres y Apellidos")
            cc = st.text_input("Documento de Identidad")
        with c2:
            mail = st.text_input("Correo Electrónico")
            tel = st.text_input("WhatsApp")
        
        if st.form_submit_button("VALIDAR E INGRESAR"):
            if nom and cc and mail and tel:
                guardar_usuario(nom, cc, mail, tel)
                st.session_state.autenticado = nom
                st.rerun()
    st.stop()

# --- INTERFAZ PRINCIPAL (YA LOGUEADO) ---
with st.sidebar:
    # AGREGAR EL LOGO (Asegúrate de que el archivo 'logo.jpg' esté en la misma carpeta)
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", width=100)
    
    st.header(f"👤 {st.session_state.autenticado}")
    if st.button("Cerrar Sesión"):
        del st.session_state.autenticado
        st.rerun()
    
    st.divider()
    st.subheader("🔑 Panel Administrativo")
    clave = st.text_input("Contraseña de César", type="password")
    if clave == "Socio2026":
        t_noticia = st.text_input("Título Noticia")
        c_noticia = st.text_area("Contenido Noticia")
        if st.button("🚀 PUBLICAR"):
            guardar_noticia(t_noticia, c_noticia, st.session_state.autenticado)
            st.rerun()

# TÍTULO PRINCIPAL EN VERDE
st.markdown("<h1 class='titulo-verde'>🚀 Búnker de Comunidad - SÍ AL MÉRITO</h1>", unsafe_allow_html=True)
noticia = cargar_noticia()

# MURO DE NOTICIAS (Letras de título en verde, contenido en blanco)
st.markdown(f"""
    <div class="noticia-box">
        <h2 style="margin:0; color: #28a745;">🔥 {noticia['titulo']}</h2>
        <p style="font-size: 20px; margin-top: 10px; color: white;">{noticia['contenido']}</p>
        <hr style="border: 0.5px solid #444;">
        <small>✍️ Autor: {noticia['autor']}</small>
    </div>
    """, unsafe_allow_html=True)

# BOTONES DE REDES
st.subheader("🔗 Nuestras Redes Oficiales")
red1, red2, red3, red4 = st.columns(4)
red1.link_button("📺 YouTube", "https://youtube.com/@sialmerito")
red2.link_button("📱 TikTok", "https://tiktok.com")
red3.link_button("💙 Facebook", "https://facebook.com")
red4.link_button("📚 Material", "https://google.com")

# CHAT
st.divider()
st.header("💬 Foro de Aspirantes")
for m in cargar_mensajes():
    with st.chat_message("user"):
        st.write(f"**{m['usuario']}** - <small>{m['fecha']}</small>", unsafe_allow_html=True)
        st.write(m['texto'])

if prompt := st.chat_input("Escribe tu duda..."):
    guardar_mensaje(st.session_state.autenticado, prompt)
    st.rerun()
