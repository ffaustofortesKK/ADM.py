import streamlit as st
from supabase import create_client

# --- CONFIGURAÇÃO DO SUPABASE ---
# Cole aqui os dados que você pegou na engrenagem (API) do Supabase
URL_SUPABASE = "SUA_URL_AQUI"
KEY_SUPABASE = "SUA_KEY_AQUI"
supabase = create_client(URL_SUPABASE, KEY_SUPABASE)

st.set_page_config(page_title="Painel de Administração")
st.title("🛡️ Painel de Controle")

# Senha de Acesso
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    senha = st.text_input("Senha:", type="password")
    if st.button("Entrar"):
        if senha == "donagay0804241708": # Sua senha
            st.session_state["logado"] = True
            st.rerun()
else:
    st.write("Conectado ao Banco de Dados com sucesso!")
    
    # Busca os prestadores no banco
    response = supabase.table("prestadores").select("*").execute()
    prestadores = response.data
    
    if not prestadores:
        st.write("Nenhum prestador cadastrado ainda.")
    else:
        for p in prestadores:
            st.write(f"Prestador: {p['nome_prestador']} | Referência: {p['referencia_pagamento']}")
            if st.checkbox(f"Liberar {p['nome_prestador']}", value=p['status_pagamento']):
                # Aqui o site avisa o Supabase que o pagamento foi confirmado
                supabase.table("prestadores").update({"status_pagamento": True}).eq("id", p['id']).execute()
                st.success("Pagamento confirmado!")
