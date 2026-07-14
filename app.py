import streamlit as st
from supabase import create_client
from datetime import datetime, timezone

# --- Configuração ---
url = st.secrets["URL_SUPABASE"]
key = st.secrets["KEY_SUPABASE"]
supabase = create_client(url, key)

st.set_page_config(page_title="Painel de Administração", layout="wide")
st.title("🛡️ Painel de Controle")

# --- LOGIN ---
if "logado" not in st.session_state: st.session_state["logado"] = False
if not st.session_state["logado"]:
    senha = st.text_input("Senha:", type="password")
    if st.button("Entrar") and senha == "1234":
        st.session_state["logado"] = True
        st.rerun()
    st.stop()

# --- SEÇÃO: FILA DE PRESTADORES ---
st.subheader("🎤 Fila de Prestadores")

if st.button("🔄 Atualizar Fila"):
    st.rerun()

try:
    # Busca os dados do Supabase
    response = supabase.table("prestadores").select("*").execute()
    prestadores = response.data
    
    if prestadores:
        # Cabeçalhos da tabela
        header1, header2, header3, header4 = st.columns([2, 2, 1, 1])
        header1.write("**Prestador**")
        header2.write("**Ref.**")
        header3.write("**Status**")
        header4.write("**Ação**")

        # Loop pelos prestadores
        for p in prestadores:
            # Chave única para cada botão baseada no ID único do Supabase
            p_id = p.get('id')
            
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            
            # Formatação segura dos nomes (evita erro de NoneType)
            nome = str(p.get('Nome') or p.get('nome') or "")
            sobrenome = str(p.get('Sobrenome') or p.get('sobrenome') or "")
            display_name = f"{nome} {sobrenome}".strip() or p.get('slug_unico') or "Sem Nome"
            
            col1.write(f"**{display_name}**")
            col2.write(str(p.get('referencia_pagamento') or "N/A"))
            
            status = p.get('status_pagamento', False)
            
            if status:
                col3.write("✅ SIM")
                col4.write("⏳ Em uso")
            else:
                col3.write("❌ NÃO")
                # Botão com chave única absoluta
                if col4.button("Pagar", key=f"btn_pagar_{p_id}"):
                    # Atualiza o status no Supabase
                    supabase.table("prestadores").update({
                        "status_pagamento": True,
                        "inicio_servico": datetime.now(timezone.utc).isoformat()
                    }).eq("id", p_id).execute()
                    # Recarrega a página para refletir a mudança
                    st.rerun()
    else:
        st.info("Nenhum prestador na fila.")
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
