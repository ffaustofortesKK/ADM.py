import streamlit as st
import qrcode
import re
from io import BytesIO
import requests

st.set_page_config(page_title="Painel do Prestador", layout="wide")

# URL BASE do Firebase
BASE_URL = "https://grupoffkaraoke-default-rtdb.firebaseio.com"
CLOUDINARY_CLOUD_NAME = "yhwgjh7g"

# Função para normalizar nome da música
def normalizar_nome(nome):
    nome = nome.replace(".mp4", "")
    nome = re.sub(r'[^\w\s]', '', nome)
    nome = "_".join(nome.split())
    return nome

# Inicialização
if "nome" not in st.session_state: st.session_state.nome = None
if "slug" not in st.session_state: st.session_state.slug = None

# --- LOGIN ---
if st.session_state.nome is None:
    st.title("🎤 Portal do Prestador")
    nome_input = st.text_input("Nome:")
    sobrenome_input = st.text_input("Sobrenome:") 
    telef = st.text_input("Telefone:")
    
    if st.button("Entrar"):
        if nome_input and sobrenome_input and telef:
            slug_unico = f"{nome_input.lower()}-{sobrenome_input.lower()}"
            
            # --- ENVIO PARA O ADM (Firebase) ---
            # Grava o prestador numa lista geral para o ADM ver
            data_prestador = {
                "nome": f"{nome_input} {sobrenome_input}",
                "telefone": telef,
                "slug_unico": slug_unico
            }
            # Usa o telefone como chave única para evitar duplicados
            requests.put(f"{BASE_URL}/prestadores/{telef.replace(' ', '')}.json", json=data_prestador)
            
            st.session_state.update({"nome": f"{nome_input} {sobrenome_input}", "slug": slug_unico})
            st.rerun()
else:
    # ... (Restante do seu código permanece igual até o final)
    st.title(f"Bem-vindo, {st.session_state.nome}!")
    # ... (Restante do seu código)
