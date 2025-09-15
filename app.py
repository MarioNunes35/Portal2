import streamlit as st
from typing import Optional

st.set_page_config(page_title="Portal Unificado – Login", layout="wide", initial_sidebar_state="collapsed")

# --------- Utils de usuário ----------
def _user_obj():
    u = getattr(getattr(st, "context", None), "user", None)
    return u if u else getattr(st, "user", None)

def user_email() -> str:
    u = _user_obj()
    if not u:
        return ""
    for k in ("email", "primaryEmail", "preferred_username"):
        v = getattr(u, k, None)
        if v:
            return str(v)
    try:
        s = str(u).strip()
        if "@" in s:
            return s
    except Exception:
        pass
    return ""

# --------- Detecta provedor nos Secrets ----------
def detect_provider() -> Optional[str]:
    auth = st.secrets.get("auth", {})
    google = auth.get("google", {})
    if google.get("client_id") and google.get("client_secret"):
        return "google"  # usa [auth.google]
    oidc = st.secrets.get("oidc", {})
    need = ["client_id", "client_secret", "redirect_uri", "discovery_url", "cookie_secret"]
    if all(oidc.get(k) for k in need):
        return "oidc"    # usa [oidc]
    return None

def show_minimal_help():
    st.write("Preencha **[auth.google]** OU **[oidc]** nos Secrets.")
    st.code(
        '[auth]\n'
        'cookie_secret="UM_TOKEN_LONGO_E_ESTAVEL"\n\n'
        '[auth.google]\n'
        'client_id="SEU_CLIENT_ID"\n'
        'client_secret="SEU_CLIENT_SECRET"\n'
        '# opcional: redirect_uri="https://SEU-APP.streamlit.app/oauth2callback"\n',
        language="toml",
    )
    st.code(
        '[oidc]\n'
        'client_id="SEU_CLIENT_ID"\n'
        'client_secret="SEU_CLIENT_SECRET"\n'
        'redirect_uri="https://SEU-APP.streamlit.app/oauth2callback"\n'
        'discovery_url="https://accounts.google.com/.well-known/openid-configuration"\n'
        'cookie_secret="UM_TOKEN_LONGO_E_ESTAVEL"\n',
        language="toml",
    )

def ensure_login() -> str:
    provider = detect_provider()
    if not provider:
        st.error("Nenhum provedor de autenticação configurado.")
        show_minimal_help()
        st.stop()
    if not user_email():
        st.login(provider)  # "google" ou "oidc"
        st.stop()
    return provider

# --------- Página ----------
def main():
    st.title("🔐 Portal Unificado – Login")
    provider = ensure_login()
    st.success(f"Login ok ({provider}).")

    # Redireciona para a página de aplicativos apenas 1 vez
    if not st.session_state.get("_redir"):
        st.session_state["_redir"] = True
        try:
            st.switch_page("pages/02_Aplicativos.py")
        except Exception:
            st.info("Abra a página **02_Aplicativos** pelo menu lateral (ícone '>').")
    else:
        try:
            st.page_link("pages/02_Aplicativos.py", label="➡️ Ir para Aplicativos")
        except Exception:
            pass

if __name__ == "__main__":
    main()




