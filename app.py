# app.py — Portal Unificado com Modo Debug
import streamlit as st
import sys

st.set_page_config(page_title="Portal Unificado", page_icon="🚀", layout="wide")

# Parâmetro de debug via URL: ?debug=true
debug_mode = st.query_params.get("debug", "false").lower() == "true"

if debug_mode:
    # MODO DEBUG
    st.title("🔍 Diagnóstico Completo - OAuth Config")
    
    # Informações do sistema
    st.markdown("### 📊 Informações do Sistema")
    st.write(f"**Streamlit Version:** {st.__version__}")
    st.write(f"**Python Version:** {sys.version}")
    
    # Verifica se st.login existe
    st.markdown("### 🔧 Disponibilidade do st.login")
    if hasattr(st, "login"):
        st.success("✅ st.login() está disponível")
    else:
        st.error("❌ st.login() NÃO está disponível")
        st.warning("Streamlit precisa ser atualizado para versão ≥ 1.40.0")
    
    # Diagnóstico detalhado dos secrets
    st.markdown("### 🔐 Diagnóstico dos Secrets")
    
    try:
        # Tenta acessar st.secrets
        secrets = st.secrets
        st.success("✅ st.secrets acessível")
        
        # Mostra as chaves principais disponíveis
        st.write("**Chaves disponíveis em st.secrets:**", list(secrets.keys()))
        
        # Verifica estrutura de auth
        if "auth" in secrets:
            st.success("✅ Seção [auth] encontrada")
            auth_section = secrets["auth"]
            st.write("**Chaves em [auth]:**", list(auth_section.keys()))
            
            # Verifica campos obrigatórios
            required_fields = {
                "redirect_uri": auth_section.get("redirect_uri"),
                "cookie_secret": auth_section.get("cookie_secret"),
                "allowed_emails": auth_section.get("allowed_emails")
            }
            
            for field, value in required_fields.items():
                if value:
                    if field == "cookie_secret":
                        st.success(f"✅ {field}: {'*' * min(len(str(value)), 20)}...")
                    else:
                        st.success(f"✅ {field}: {value}")
                else:
                    st.error(f"❌ {field}: AUSENTE ou VAZIO")
            
            # Verifica seção google
            if "google" in auth_section:
                st.success("✅ Seção [auth.google] encontrada")
                google_section = auth_section["google"]
                st.write("**Chaves em [auth.google]:**", list(google_section.keys()))
                
                google_fields = {
                    "client_id": google_section.get("client_id"),
                    "client_secret": google_section.get("client_secret"),
                    "server_metadata_url": google_section.get("server_metadata_url")
                }
                
                for field, value in google_fields.items():
                    if value:
                        if field == "client_secret":
                            st.success(f"✅ {field}: GOCSPX-{'*' * 20}...")
                        else:
                            st.success(f"✅ {field}: {value}")
                    else:
                        st.error(f"❌ {field}: AUSENTE ou VAZIO")
            else:
                st.error("❌ Seção [auth.google] NÃO encontrada")
        else:
            st.error("❌ Seção [auth] NÃO encontrada")
            
    except Exception as e:
        st.error(f"❌ Erro ao acessar secrets: {str(e)}")
        st.code(str(e))
    
    # Template do secrets correto
    st.markdown("### 📝 Template Correto do secrets.toml")
    
    template = """[auth]
redirect_uri = "https://f4iu25yf4y6qdhjisk6bqy.streamlit.app/oauth2callback"
cookie_secret = "Hc2RzH1m8w1v7h4A0z3Fv4uYw8PV6Xw2Vq9l2"
allowed_emails = ["mariobnunes34@gmail.com", "mark.ivo.sm@gmail.com"]

[auth.google]
client_id = "402896734132-s3u3ii39dddarnft4qr04fb6n69.apps.googleusercontent.com"
client_secret = "GOCSPX-mqTySo-fPDpfVUSjVyqG2e"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
"""
    
    st.code(template, language="toml")
    
    # Teste da função check_oidc_config
    st.markdown("### 🧪 Teste da Validação OAuth")
    
    def test_check_oidc_config():
        problems = []
        
        try:
            auth = st.secrets.get("auth", {})
            provider = auth.get("google", {})

            if not hasattr(st, "login"):
                problems.append("❌ Esta versão do Streamlit não possui st.login()")

            for k in ("redirect_uri", "cookie_secret"):
                if not str(auth.get(k, "")).strip():
                    problems.append(f"❌ [auth].{k} ausente nos secrets")

            for k in ("client_id", "client_secret", "server_metadata_url"):
                if not str(provider.get(k, "")).strip():
                    problems.append(f"❌ Parâmetro OAuth ausente: {k} (em [auth.google])")

            ru = str(auth.get("redirect_uri", "")).strip()
            if ru and not ru.endswith("/oauth2callback"):
                problems.append("❌ redirect_uri deve terminar com /oauth2callback")

        except Exception as e:
            problems.append(f"❌ Erro ao acessar secrets: {str(e)}")

        return problems

    problems = test_check_oidc_config()

    if problems:
        st.error("⚠️ Problemas encontrados:")
        for problem in problems:
            st.write(f"- {problem}")
    else:
        st.success("🎉 Configuração OAuth válida!")

    # Link para voltar ao modo normal
    st.markdown("---")
    st.markdown("🔙 [Voltar ao Portal Normal](https://f4iu25yf4y6qdhjisk6bqy.streamlit.app)")
    
    st.stop()  # Para aqui no modo debug

# RESTO DO CÓDIGO ORIGINAL (modo normal)
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
        
        # Link para modo debug
        st.markdown("---")
        st.markdown("### 🔍 **Diagnóstico Detalhado:**")
        st.markdown("🔗 [Clique aqui para diagnóstico completo](https://f4iu25yf4y6qdhjisk6bqy.streamlit.app?debug=true)")
        
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
    
    # Redireciona para a página de aplicativos
    st.switch_page("pages/02_Aplicativos.py")

else:
    st.warning("⚠️ Não foi possível obter informações do usuário. Tente fazer login novamente.")
