import streamlit as st
import requests

# URL do seu Firebase
BASE_URL = "https://grupoffkaraoke-default-rtdb.firebaseio.com"

st.title("Painel do Administrador")

# Lê a lista de prestadores do Firebase
url_prestadores = f"{BASE_URL}/prestadores.json"
try:
    response = requests.get(url_prestadores)
    prestadores = response.json()
    
    if prestadores:
        st.write("### Prestadores Registados:")
        for tel, dados in prestadores.items():
            st.write(f"👤 **{dados['nome']}** - Tel: {tel}")
    else:
        st.write("Nenhum prestador registado ainda.")
except Exception as e:
    st.error(f"Erro ao carregar prestadores: {e}")
