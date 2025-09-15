# app.py — Portal Unificado (login + roteamento)
import streamlit as st
from urllib.parse import urlparse

st.set_page_config(page_title="Portal Unificado", page_icon="🔐", layout="wide")

def check_oidc_config():
    problems = []
    auth = st.secrets.get("auth", {})
    provider = st.secrets.get("auth", {}).get("google", st.secrets.get("auth", {}))

    if not hasattr(st, "login"):
        problems.append("Esta versão do Streamlit não possui st.login(). Atualize o Streamlit.")

    for k in ("redirect_uri", "cookie_secret"):
        if not str(auth.get(k, "")).strip():
            problems.append(f"[auth].{k} ausente nos secrets.")

    for k in ("client_id", "client_secret", "server_metadata_url"):
        if not str(provider.get(k, "")).strip():
            problems.append(f"Parâmetro OAuth ausente: {k} (em [auth.google]).")

    # Sanity do redirect_uri
    ru = str(auth.get("redirect_uri", "")).strip()
    if ru and not ru.endswith("/oauth2callback"):
        problems.append("redirect_uri deve terminar com /oauth2callback")

    if problems:
        st.error("⚠️ Configuração de autenticação incompleta:")
        for p in problems:
            st.markdown(f"- {p}")
        st.stop()

def is_allowed(email: str) -> bool:
    if not email:
        return False
    allowed_emails = set(st.secrets.get("auth", {}).get("allowed_emails", []))
    allowed_domains = set(st.secrets.get("auth", {}).get("allowed_domains", []))
    if not allowed_emails and not allowed_domains:
        # Sem allowlist => libera todo mundo autenticado
        return True
    email = email.strip().lower()
    domain = email.split("@")[-1] if "@" in email else ""
    return (email in allowed_emails) or (domain in allowed_domains)

def get_user_email() -> str:
    # Em versões recentes, st.login() popula st.context.user or st.session_state.
    # Tentamos múltiplas fontes para robustez.
    u = getattr(st, "context", None)
    if u and getattr(u, "user", None):
        # Em geral, u.user é um objeto. Tentamos .email / ['email'] / .get('email')
        for key in ("email", "primaryEmail", "preferred_username"):
            try:
                val = getattr(u.user, key, None) or u.user.get(key, None)
            except Exception:
                val = None
            if val:
                return str(val)
    # Telas antigas / fallback (alguns forks colocam em session_state)
    for key in ("user_email", "email", "oidc_email"):
        if key in st.session_state and st.session_state[key]:
            return str(st.session_state[key])
    return ""

check_oidc_config()

st.title("🔐 Portal Unificado")
st.caption("Login único → redireciona para a página de aplicativos sem pedir novo login.")

# Exibe o widget de login; após sucesso, continua
try:
    # Algumas versões aceitam st.login() sem argumentos; outras suportam "oidc".
    try:
        st.login()
    except TypeError:
        st.login()
except Exception as e:
    st.error("Falha ao exibir o login (st.login). Verifique a versão do Streamlit e os secrets.")
    st.exception(e)
    st.stop()

# Após autenticar, implementamos a allowlist (se existir)
email = get_user_email()
if not is_allowed(email):
    st.error("Acesso negado. Seu e-mail não está autorizado nesta aplicação. 🚫")
    st.write("Se você acredita que isso é um engano, contate o administrador para adicionar seu e-mail/domínio em `allowed_emails`/`allowed_domains`.")
    st.stop()

# Usuário autorizado → redireciona para a página de aplicativos
st.success(f"Login concluído para **{email or 'usuário'}**. Redirecionando…")
# Redireciona para pages/02_Aplicativos.py (sem abrir nova aba, sem exigir novo login)
st.switch_page("pages/02_Aplicativos.py")
