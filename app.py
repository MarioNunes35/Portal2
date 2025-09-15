# app.py — Portal Unificado (login + roteamento)
import streamlit as st

st.set_page_config(page_title="Portal Unificado", page_icon="🚀", layout="wide")

def check_oidc_config():
    """Verifica se a configuração OIDC está completa."""
    problems = []
    
    try:
        auth = st.secrets.get("auth", {})
        provider = auth.get("google", {})

        # Verifica se st.login está disponível
        if not hasattr(st, "login"):
            problems.append("❌ Esta versão do Streamlit não possui st.login(). Atualize o Streamlit.")

        # Verifica configurações básicas de auth
        for k in ("redirect_uri", "cookie_secret"):
            if not str(auth.get(k, "")).strip():
                problems.append(f"❌ [auth].{k} ausente nos secrets.")

        # Verifica configurações do Google OAuth
        for k in ("client_id", "client_secret", "server_metadata_url"):
            if not str(provider.get(k, "")).strip():
                problems.append(f"❌ Parâmetro OAuth ausente: {k} (em [auth.google]).")

        # Valida o redirect_uri
        ru = str(auth.get("redirect_uri", "")).strip()
        if ru and not ru.endswith("/oauth2callback"):
            problems.append("❌ redirect_uri deve terminar com /oauth2callback")

    except Exception as e:
        problems.append(f"❌ Erro ao acessar secrets: {str(e)}")

    if problems:
        st.error("⚠️ **Configuração de autenticação incompleta:**")
        for p in problems:
            st.markdown(f"- {p}")
        
        # Instruções para configuração
        st.markdown("---")
        st.markdown("### 📋 **Como configurar:**")
        st.markdown("""
        1. **Crie um arquivo `.streamlit/secrets.toml`** no seu projeto
        2. **Configure as credenciais do Google OAuth** no [Google Cloud Console](https://console.cloud.google.com)
        3. **Adicione as configurações** conforme o exemplo abaixo
        """)
        
        with st.expander("📄 Exemplo de secrets.toml"):
            st.code("""
[auth]
redirect_uri = "https://your-app-url.streamlit.app/oauth2callback"
cookie_secret = "your-random-secret-key-here-32-chars-min"
allowed_emails = ["email1@gmail.com", "email2@empresa.com"]

[auth.google]
client_id = "your-google-client-id.apps.googleusercontent.com"
client_secret = "your-google-client-secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid_configuration"
            """, language="toml")
        
        st.stop()

def is_allowed(email: str) -> bool:
    """Verifica se o email está autorizado."""
    if not email:
        return False
    
    try:
        auth = st.secrets.get("auth", {})
        allowed_emails = set(str(e).strip().lower() for e in auth.get("allowed_emails", []))
        allowed_domains = set(str(d).strip().lower() for d in auth.get("allowed_domains", []))
        
        # Se não há allowlist, permite todos os autenticados
        if not allowed_emails and not allowed_domains:
            return True
        
        email = email.strip().lower()
        domain = email.split("@")[-1] if "@" in email else ""
        
        return email in allowed_emails or domain in allowed_domains
    except Exception:
        return True  # Fallback: permite em caso de erro

def get_user_email() -> str:
    """Obtém o email do usuário autenticado."""
    try:
        # Método moderno
        if hasattr(st, "context") and hasattr(st.context, "user") and st.context.user:
            user = st.context.user
            for key in ("email", "primaryEmail", "preferred_username"):
                if hasattr(user, key):
                    email = getattr(user, key)
                    if email:
                        return str(email)
                elif isinstance(user, dict) and key in user:
                    email = user[key]
                    if email:
                        return str(email)
        
        # Fallback para session_state
        for key in ("user_email", "email", "oidc_email"):
            if key in st.session_state and st.session_state[key]:
                return str(st.session_state[key])
    except Exception:
        pass
    
    return ""

# CSS para estilização
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.main-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 2rem;
    text-align: center;
}

.login-card {
    background: rgba(255, 255, 255, 0.95);
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
}

.title {
    font-size: 2.5rem;
    font-weight: bold;
    color: #333;
    margin-bottom: 0.5rem;
}

.subtitle {
    color: #666;
    font-size: 1.1rem;
    margin-bottom: 2rem;
}

.feature-list {
    text-align: left;
    color: #555;
    margin: 1.5rem 0;
}

.feature-list li {
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# Verifica configuração antes de prosseguir
check_oidc_config()

# Interface principal
st.markdown("""
<div class="main-container">
    <div class="login-card">
        <div class="title">🚀 Portal Unificado</div>
        <div class="subtitle">Acesso centralizado aos seus aplicativos de análise</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🔐 **Autenticação**")
st.info("👇 Clique no botão abaixo para fazer login com sua conta Google")

# Exibe o widget de login
try:
    # Tenta fazer login com OIDC
    if hasattr(st, "login"):
        try:
            st.login("oidc")
        except TypeError:
            # Fallback para versões mais antigas
            st.login()
        except Exception as e:
            if "missing for the authentication provider" in str(e):
                st.error("❌ **Configuração OAuth incompleta.** Verifique o arquivo `secrets.toml`.")
            else:
                st.error(f"❌ **Erro no login:** {str(e)}")
            st.stop()
    else:
        st.error("❌ **st.login() não disponível.** Atualize o Streamlit para a versão mais recente.")
        st.stop()

except Exception as e:
    st.error("❌ **Falha ao exibir o login.** Verifique a configuração.")
    st.exception(e)
    st.stop()

# Após autenticar com sucesso
email = get_user_email()

if email:
    # Verifica se o usuário está autorizado
    if not is_allowed(email):
        st.error("🚫 **Acesso Negado**")
        st.warning(f"Seu e-mail **{email}** não está autorizado nesta aplicação.")
        st.info("💡 Entre em contato com o administrador para adicionar seu e-mail/domínio à lista de usuários autorizados.")
        st.stop()

    # Usuário autorizado - redireciona para aplicativos
    st.success(f"✅ **Login concluído para:** {email}")
    st.info("🔄 Redirecionando para seus aplicativos...")
    
    # Pequeno delay para melhor UX
    import time
    time.sleep(1)
    
    # Redireciona para a página de aplicativos
    st.switch_page("pages/02_Aplicativos.py")

else:
    st.warning("⚠️ Não foi possível obter informações do usuário. Tente fazer login novamente.")
