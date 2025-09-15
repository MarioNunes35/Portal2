# app.py - App Principal com Redirecionamento Automático
import streamlit as st
import time

# --- Configuração da Página ---
st.set_page_config(
    page_title="Portal de Análises - Login", 
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Estilo CSS ---
LOGIN_CSS = """
<style>
.stApp {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.login-container {
    display: flex; align-items: center; justify-content: center; 
    min-height: 100vh; text-align: center;
}

.login-box {
    background: rgba(255,255,255,0.1); backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.2); border-radius: 20px;
    padding: 60px 40px; box-shadow: 0 25px 50px rgba(0,0,0,0.3);
    max-width: 500px; width: 90vw;
}

.login-box h1 {
    margin-bottom: 10px; font-size: 2.5rem; font-weight: 700;
}

.login-box p {
    opacity: 0.9; margin-bottom: 30px; font-size: 1.1rem;
}

.stButton button {
    background: rgba(255,255,255,0.2) !important;
    border: 2px solid rgba(255,255,255,0.3) !important;
    color: white !important; border-radius: 15px !important;
    padding: 15px 30px !important; font-size: 18px !important;
    font-weight: 600 !important; transition: all 0.3s ease !important;
    width: 100% !important; height: 60px !important;
}

.stButton button:hover {
    background: rgba(255,255,255,0.3) !important;
    border-color: rgba(255,255,255,0.5) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
}

.success-message {
    background: rgba(76, 175, 80, 0.2); border: 1px solid rgba(76, 175, 80, 0.4);
    border-radius: 10px; padding: 20px; margin: 20px 0;
}

.redirect-message {
    background: rgba(33, 150, 243, 0.2); border: 1px solid rgba(33, 150, 243, 0.4);
    border-radius: 10px; padding: 20px; margin: 20px 0; text-align: center;
}

.loading-spinner {
    display: inline-block; width: 20px; height: 20px;
    border: 3px solid rgba(255,255,255,0.3); border-radius: 50%;
    border-top-color: white; animation: spin 1s ease-in-out infinite;
    margin-right: 10px;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.manual-link {
    display: inline-block; background: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.3); border-radius: 10px;
    padding: 15px 25px; color: white; text-decoration: none;
    font-weight: 600; margin-top: 15px; transition: all 0.3s ease;
}

.manual-link:hover {
    background: rgba(255,255,255,0.3); transform: translateY(-2px);
    color: white; text-decoration: none;
}
</style>
"""

st.markdown(LOGIN_CSS, unsafe_allow_html=True)

# --- Configurações ---
PORTAL_URL = "https://subaplicativos.streamlit.app"
REDIRECT_DELAY = 3  # segundos

# --- Funções de Autenticação ---
def is_authenticated():
    """Verifica se o usuário está autenticado."""
    try:
        # Verifica diferentes métodos de autenticação do Streamlit
        if hasattr(st, 'context') and hasattr(st.context, 'user') and st.context.user:
            return True
        if hasattr(st, 'user') and st.user:
            return True
        # Verifica session_state
        for key in ("authenticated", "user_email", "email"):
            if key in st.session_state and st.session_state[key]:
                return True
    except Exception:
        pass
    return False

def get_user_email():
    """Obtém o email do usuário autenticado."""
    try:
        # Método moderno
        if hasattr(st, 'context') and hasattr(st.context, 'user') and st.context.user:
            user = st.context.user
            for key in ("email", "primaryEmail", "preferred_username"):
                if hasattr(user, key):
                    email = getattr(user, key)
                    if email:
                        return str(email)
        
        # Método legado
        if hasattr(st, 'user') and st.user:
            if hasattr(st.user, 'email') and st.user.email:
                return str(st.user.email)
        
        # Session state
        for key in ("user_email", "email"):
            if key in st.session_state and st.session_state[key]:
                return str(st.session_state[key])
    except Exception:
        pass
    return ""

def is_allowed(email):
    """Verifica se o email está autorizado."""
    if not email:
        return False
    
    try:
        auth_config = st.secrets.get("auth", {})
        allowed_emails = set(str(e).strip().lower() for e in auth_config.get("allowed_emails", []))
        allowed_domains = set(str(d).strip().lower() for d in auth_config.get("allowed_domains", []))
        
        if not allowed_emails and not allowed_domains:
            return True
        
        email = email.strip().lower()
        domain = email.split("@")[-1] if "@" in email else ""
        
        return email in allowed_emails or domain in allowed_domains
    except Exception:
        return True

def render_login_page():
    """Renderiza a página de login."""
    st.markdown('''
        <div class="login-container">
            <div class="login-box">
                <h1>🚀 Portal de Análises</h1>
                <p>Faça login para acessar seus aplicativos de análise</p>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Botão de login centralizado
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔐 Entrar com Google", key="login_btn"):
            # O Streamlit Cloud processará automaticamente o OAuth
            st.rerun()

def render_success_and_redirect():
    """Renderiza página de sucesso e redireciona automaticamente."""
    user_email = get_user_email()
    
    st.markdown(f'''
        <div class="login-container">
            <div class="login-box">
                <div class="success-message">
                    <h2>✅ Login Realizado com Sucesso!</h2>
                    <p><strong>Bem-vindo:</strong> {user_email or "Usuário"}</p>
                </div>
                
                <div class="redirect-message">
                    <div class="loading-spinner"></div>
                    <strong>Redirecionando para o Portal de Aplicativos...</strong>
                    <p style="margin-top: 10px; opacity: 0.8;">
                        Você será redirecionado automaticamente em {REDIRECT_DELAY} segundos
                    </p>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # JavaScript para redirecionamento automático
    st.markdown(f"""
    <script>
        setTimeout(function() {{
            window.location.href = "{PORTAL_URL}";
        }}, {REDIRECT_DELAY * 1000});
    </script>
    """, unsafe_allow_html=True)
    
    # Link manual caso o redirecionamento automático falhe
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <a href="{PORTAL_URL}" target="_self" class="manual-link">
            🚀 Ir para Portal de Aplicativos
        </a>
        """, unsafe_allow_html=True)

def render_access_denied():
    """Renderiza página de acesso negado."""
    user_email = get_user_email()
    
    st.markdown(f'''
        <div class="login-container">
            <div class="login-box">
                <h2>🚫 Acesso Negado</h2>
                <p>O email <strong>{user_email}</strong> não tem permissão para acessar este portal.</p>
                <p style="opacity: 0.8;">Entre em contato com o administrador para solicitar acesso.</p>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Tentar Novamente", key="retry_btn"):
            # Limpa sessão e tenta novamente
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# --- Lógica Principal ---
def main():
    """Função principal do app."""
    try:
        # Verifica se está autenticado
        if not is_authenticated():
            render_login_page()
            return
        
        # Obtém email do usuário
        user_email = get_user_email()
        
        # Verifica permissões
        if user_email and not is_allowed(user_email):
            render_access_denied()
            return
        
        # Usuário autenticado e autorizado - redireciona
        render_success_and_redirect()
        
    except Exception as e:
        st.error("⚠️ Erro inesperado na aplicação")
        st.exception(e)
        
        if st.button("🔄 Recarregar", key="reload_btn"):
            st.rerun()

if __name__ == "__main__":
    main()
