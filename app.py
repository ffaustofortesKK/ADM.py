import streamlit as st

# Título do Painel
st.set_page_config(page_title="Painel de Administração", layout="centered")

st.title("🛡️ Painel de Controle - Administração")

# Configuração da senha
SENHA_ADMIN = "donagay0804241708" # Mude aqui para a senha que você desejar

def pagina_de_login():
    st.subheader("Acesso Restrito")
    senha = st.text_input("Digite a senha de administrador:", type="password")
    if st.button("Entrar"):
        if senha == SENHA_ADMIN:
            st.session_state['logado'] = True
            st.rerun()
        else:
            st.error("Senha incorreta!")

def pagina_principal():
    st.success("Bem-vindo ao Painel de Controle!")
    st.write("Aqui você poderá gerenciar os prestadores e validar pagamentos.")
    
    # Exemplo de lista de prestadores (futuramente conectaremos ao Supabase)
    st.subheader("Lista de Prestadores")
    prestadores = ["Prestador 01", "Prestador 02", "Prestador 03"]
    
    for nome in prestadores:
        col1, col2 = st.columns([2, 1])
        col1.write(f"Prestador: {nome}")
        if col2.button(f"Confirmar Pagamento", key=nome):
            st.write(f"✅ Pagamento de {nome} confirmado!")

# Lógica de controle de acesso
if 'logado' not in st.session_state:
    st.session_state['logado'] = False

if st.session_state['logado']:
    pagina_principal()
    if st.button("Sair"):
        st.session_state['logado'] = False
        st.rerun()
else:
    pagina_de_login()
