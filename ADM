import streamlit as st
from supabase import create_client
from datetime import datetime, timezone
from streamlit_autorefresh import st_autorefresh

# Configuração
url = st.secrets["URL_SUPABASE"]
key = st.secrets["KEY_SUPABASE"]
supabase = create_client(url, key)

# Atualiza a página a cada 5 segundos (1 segundo é muito rápido e causa instabilidade nos cliques)
st_autorefresh(interval=5000, key="datarefresh")

st.set_page_config(page_title="Painel de Administração", layout="wide")
st.title("🛡️ Painel de Controle")

# --- LOGIN ---
if "logado" not in st.session_state: st.session_state["logado"] = False

if not st.session_state["logado"]:
    senha = st.text_input("Senha:", type="password")
    if st.button("Entrar") and senha == "1234":
        st.session_state["logado"] = True
        st.rerun()
    st.stop() # Para a execução se não estiver logado

# --- ÁREA LOGADA ---
if st.button("Sair"):
    st.session_state["logado"] = False
    st.rerun()

# --- SEÇÃO 1: PEDIDOS WEB ---
st.subheader("📥 Pedidos Web Recebidos")
try:
    pedidos = supabase.table("pedidos_pendentes").select("*").eq("status", "pendente").execute().data
    
    if pedidos:
        for p in pedidos:
            col_a, col_b = st.columns([4, 1])
            col_a.write(f"🎤 **{p.get('cantor', 'Sem nome')}** - 🎵 {p.get('musica', 'Sem nome')}")
            if col_b.button("Aprovar", key=f"aprove_{p['id']}"):
                slug = p['cantor'].lower().replace(" ", "-")
                supabase.table("prestadores").insert({
                    "nome_prestador": p['cantor'],
                    "referencia_pagamento": p['musica'],
                    "status_pagamento": False,
                    "slug_unico": slug,
                    "senha_acesso": "1234",
                    "status_acesso": "ativo"
                }).execute()
                supabase.table("pedidos_pendentes").delete().eq("id", p['id']).execute()
                st.rerun()
    else:
        st.info("Nenhum pedido novo.")
except Exception as e:
    st.error(f"Erro ao buscar pedidos: {e}")

st.divider()

# --- SEÇÃO 2: FILA DE PRESTADORES ---
st.subheader("🎤 Fila de Prestadores")
try:
    prestadores = supabase.table("prestadores").select("*").execute().data
    if prestadores:
        header1, header2, header3, header4 = st.columns([2, 2, 1, 1])
        header1.write("**Prestador**"); header2.write("**Ref.**"); header3.write("**Pagamento**"); header4.write("**Tempo**")

        for p in prestadores:
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            col1.write(p.get('nome_prestador', ''))
            col2.write(p.get('referencia_pagamento', ''))
            
            status = p.get('status_pagamento', False)
            inicio_str = p.get('inicio_servico')
            
            if status and inicio_str:
                inicio = datetime.fromisoformat(inicio_str.replace('Z', '+00:00'))
                agora = datetime.now(timezone.utc)
                restante = 7200 - (agora - inicio).total_seconds()
                if restante > 0:
                    m, s = divmod(int(restante), 60)
                    col3.write("✅ SIM")
                    col4.write(f"⏳ {m:02d}m {s:02d}s")
                else:
                    supabase.table("prestadores").update({"status_pagamento": False, "inicio_servico": None}).eq("id", p['id']).execute()
                    st.rerun()
            else:
                col3.write("❌ NÃO")
                if col4.button("Pagar", key=f"btn_{p['id']}"):
                    supabase.table("prestadores").update({
                        "status_pagamento": True, 
                        "inicio_servico": datetime.now(timezone.utc).isoformat()
                    }).eq("id", p['id']).execute()
                    st.rerun()
    else:
        st.write("Nenhum prestador cadastrado.")
except Exception as e:
    st.error(f"Erro ao buscar prestadores: {e}")
