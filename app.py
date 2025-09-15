# app.py - Portal Unificado (Versão Robusta)
import streamlit as st
import hashlib
import sys

st.set_page_config(page_title="Portal Unificado", page_icon="🚀", layout="wide")

# ===========================
# Session State Management
# ===========================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# ===========================
# OIDC preflight (checks Secrets before calling st.login)
# ===========================
def check_oidc_available():
    """Verifica se OIDC está disponível e configurado. 
    Retorna (available: bool, provider_arg: str|None, problems: list[str]).
    """
    problems = []
    try:
        # 1) st.login disponível?
        if not hasattr(st, "login"):
            return False, None, ["st.login não está disponível nesta versão do Streamlit"]
        
        # 2) Já logado?
        if hasattr(st, "user") and getattr(st.user, 'is_logged_in', False):
            return True, None, []
        
        # 3) Resolver provider a partir de secrets
        provider_arg, provider_problems = "google", []
        problems.extend(provider_problems)
        if problems:
            return False, provider_arg, problems
        
        return True, provider_arg, []
    except Exception as e:
        return False, None, [f"Erro ao verificar OIDC: {str(e)}"]

def resolve_auth_provider():
    """Inspeciona st.secrets e tenta descobrir onde estão as chaves de OIDC/OAuth."""
    problems = []
    auth_root = st.secrets.get("auth", {})
    
    # normalizar discovery_url -> server_metadata_url quando aparecer
    def norm_provider(cfg: dict) -> dict:
        cfg = dict(cfg or {})
        if "server_metadata_url" not in cfg and "discovery_url" in cfg:
            cfg["server_metadata_url"] = cfg.get("discovery_url")
        return cfg
    
    # 1) Caso A: tudo em [auth]
    root_cfg = norm_provider(auth_root)
    root_has_provider = all(str(root_cfg.get(k, "")).strip() for k in ("client_id","client_secret","server_metadata_url"))
    root_has_root = all(str(root_cfg.get(k, "")).strip() for k in ("redirect_uri","cookie_secret"))
    if root_has_provider and root_has_root:
        return None, []
    
    # 2) Caso B: provider nomeado dentro de [auth.<nome>]
    named_candidate = None
    for name, cfg in auth_root.items():
        if isinstance(cfg, dict):
            cfg = norm_provider(cfg)
            if all(str(cfg.get(k, "")).strip() for k in ("client_id","client_secret","server_metadata_url")):
                named_candidate = name
                break
    if named_candidate:
        if not all(str(auth_root.get(k, "")).strip() for k in ("redirect_uri","cookie_secret")):
            miss = [k for k in ("redirect_uri","cookie_secret") if not str(auth_root.get(k, "")).strip()]
            problems.append("Faltando em [auth]: " + ", ".join(miss))
        return str(named_candidate), problems
    
    # 3) Caso C: bloco legado [oidc]
    legacy = norm_provider(st.secrets.get("oidc", {}))
    if legacy:
        req = ["client_id","client_secret","redirect_uri","server_metadata_url","cookie_secret"]
        miss = [k for k in req if not str(legacy.get(k, "")).strip()]
        if miss:
            problems.append("Faltando em [oidc]: " + ", ".join(miss))
        else:
            return "oidc", []
    
    # 4) Não encontrado
    if not problems:
        problems.append("Nenhuma configuração válida encontrada. Preencha [auth] e/ou [auth.<nome>] com as chaves necessárias.")
    return None, problems

# ===========================
# Fallback Authentication
# ===========================
def simple_auth(username: str, password: str) -> tuple[bool, str]:
    """Autenticação simples como fallback"""
    fallback_users = st.secrets.get("fallback_auth", {}).get("users", {})
    
    if not fallback_users:
        fallback_users = {
            "admin": {
                "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
                "email": "admin@portal.local",
            }
        }
    
    if username in fallback_users:
        user_data = fallback_users[username]
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_hash == user_data.get("password_hash"):
            return True, user_data.get("email", f"{username}@portal.local")
    
    return False, ""

# ===========================
# Allowlist / Roles
# ===========================
def get_allowlists():
    """Carrega as listas de permissão dos secrets de forma segura."""
    auth = st.secrets.get("auth", {})
    
    allowed_emails_list = auth.get("allowed_emails", [])
    if not isinstance(allowed_emails_list, list):
        allowed_emails_list = []

    allowed_domains_list = auth.get("allowed_domains", [])
    if not isinstance(allowed_domains_list, list):
        allowed_domains_list = []

    emails = { (e or "").strip().lower() for e in allowed_emails_list }
    domains = { (d or "").strip().lower() for d in allowed_domains_list }
    return emails, domains

def is_allowed(email: str, emails: set[str], domains: set[str]):
    email = (email or "").strip().lower()
    if not emails and not domains:
        return True
    if email in emails:
        return True
    return any(email.endswith(f"@{d}") for d in domains)

# ===========================
# Styles
# ===========================
CSS = """
<style>
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-wrap {
    max-width: 600px; margin: 3rem auto 1.5rem auto;
    padding: 2rem; background: rgba(255, 255, 255, 0.95);
    border-radius: 20px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px); text-align: center;
}

.login-title {
    font-size: 2.5rem; font-weight: bold; color: #333; margin-bottom: 0.5rem;
}

.login-sub { 
    color: #666; font-size: 1.1rem; margin-bottom: 2rem; 
}

.google-btn { 
    margin-top: 1rem; 
}

.error-box {
    background: rgba(220, 53, 69, 0.1); border: 1px solid rgba(220, 53, 69, 0.3);
    border-radius: 8px; padding: 1rem; margin: 1rem 0; color: #721c24;
}

.debug-link {
    margin-top: 1rem; font-size: 0.9rem;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ===========================
# Login Functions
# ===========================
def render_login_card():
    """Renderiza o card de login com suporte a OIDC ou fallback"""
    
    st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🚀 Portal Unificado</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-sub">Acesso centralizado aos seus aplicativos de análise</div>', unsafe_allow_html=True)
    
    oidc_available, provider_arg, problems = check_oidc_available()
    
    if oidc_available and hasattr(st, 'login'):
        # OAuth disponível - mostra botão do Google
        st.markdown("### 🔐 **Autenticação**")
        st.info("👇 Clique no botão abaixo para fazer login com sua conta Google")
        
        try:
            # Chama st.login com ou sem provider_arg
            if provider_arg:
                st.login(provider_arg)
            else:
                st.login()
        except Exception as e:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.error(f"❌ **Erro no login:** {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Link para diagnóstico
            st.markdown('<div class="debug-link">', unsafe_allow_html=True)
            st.markdown("🔍 [Diagnóstico Detalhado](https://f4iu25yf4y6qdhjisk6bqy.streamlit.app?debug=true)")
            st.markdown('</div>', unsafe_allow_html=True)
            
    else:
        # OAuth não disponível - mostra problemas e fallback
        st.markdown("### ⚠️ **Configuração OAuth**")
        
        if problems:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.warning("**Login Google não disponível.** Problemas encontrados:")
            for p in problems:
                st.markdown(f"- {p}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Link para diagnóstico
            st.markdown('<div class="debug-link">', unsafe_allow_html=True)
            st.markdown("🔍 [Diagnóstico Completo](https://f4iu25yf4y6qdhjisk6bqy.streamlit.app?debug=true)")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Fallback para autenticação simples
        st.markdown("### 🔑 **Login Alternativo**")
        st.info("Use as credenciais de fallback enquanto o OAuth é configurado")
        
        with st.form("login_form"):
            username = st.text_input("Usuário", placeholder="Digite: admin")
            password = st.text_input("Senha", type="password", placeholder="Digite: admin123")
            submitted = st.form_submit_button("Entrar", type="primary", use_container_width=True)
            
            if submitted:
                if username and password:
                    success, email = simple_auth(username, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.rerun()
                    else:
                        st.error("Usuário ou senha incorretos")
                else:
                    st.error("Por favor, preencha todos os campos")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===========================
# Debug Mode
# ===========================
debug_mode = st.query_params.get("debug", "false").lower() == "true"

if debug_mode:
    # MODO DEBUG - Diagnóstico completo
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
    
    # Teste da configuração
    st.markdown("### 🧪 Teste da Configuração OAuth")
    oidc_available, provider_arg, problems = check_oidc_available()
    
    if problems:
        st.error("⚠️ Problemas encontrados:")
        for problem in problems:
            st.write(f"- {problem}")
    else:
        st.success("🎉 Configuração OAuth válida!")
        st.write(f"**Provider:** {provider_arg or 'padrão'}")
    
    # Mostra secrets (mascarados)
    st.markdown("### 🔐 Secrets Detectados")
    try:
        auth = st.secrets.get("auth", {})
        st.write("**Chaves em [auth]:**", list(auth.keys()))
        
        for key, value in auth.items():
            if isinstance(value, dict):
                st.write(f"**[auth.{key}]:**", list(value.keys()))
            elif key in ("client_secret", "cookie_secret"):
                st.write(f"**{key}:** {'*' * 20}...")
            else:
                st.write(f"**{key}:** {value}")
                
    except Exception as e:
        st.error(f"Erro ao acessar secrets: {e}")
    
    # Template correto
    st.markdown("### 📝 Template Correto")
    st.code("""[auth]
redirect_uri = "https://f4iu25yf4y6qdhjisk6bqy.streamlit.app/oauth2callback"
cookie_secret = "Hc2RzH1m8w1v7h4A0z3Fv3v4uYw8PV6Xw2Vq9l2"
allowed_emails = ["mariobnunes34@gmail.com", "mark.ivo.sm@gmail.com"]

[auth.google]
client_id = "402896734132-s3u3ii39dddarnft4qr04fb6n69.apps.googleusercontent.com"
client_secret = "GOCSPX-mqTySo-fPDpfVUSjVyqG2e"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
""", language="toml")
    
    st.markdown("---")
    st.markdown("🔙 [Voltar ao Portal](https://f4iu25yf4y6qdhjisk6bqy.streamlit.app)")
    st.stop()

# ===========================
# Main Application Logic
# ===========================

# Determina se está logado
is_logged_in = False
user_email = None

if hasattr(st, 'user') and getattr(st.user, 'is_logged_in', False):
    is_logged_in = True
    user_email = (getattr(st.user, 'email', '') or '').lower()
elif st.session_state.authenticated:
    is_logged_in = True
    user_email = st.session_state.user_email

# Se não está logado, mostra a tela de login e para a execução
if not is_logged_in:
    render_login_card()
    st.stop()

# A partir daqui, o usuário está logado.
# Verifica permissões de acesso
emails, domains = get_allowlists()
if not is_allowed(user_email, emails, domains):
    st.error("🚫 **Acesso Negado**")
    st.warning(f"Seu e-mail **{user_email}** não está autorizado nesta aplicação.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Sair", type="primary", use_container_width=True):
            if hasattr(st, 'logout'):
                st.logout()
            else:
                st.session_state.authenticated = False
                st.session_state.user_email = None
                st.rerun()
    st.stop()

# Usuário autorizado - redireciona para aplicativos
st.success(f"✅ **Login concluído para:** {user_email}")
st.info("🔄 Redirecionando para seus aplicativos...")

# Redireciona para a página de aplicativos
st.switch_page("pages/02_Aplicativos.py")
