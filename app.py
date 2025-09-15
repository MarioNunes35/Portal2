import streamlit as st
from typing import Dict, Tuple

st.set_page_config(
    page_title="Portal Unificado – Login",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------- Utilitários de usuário/autenticação -----------------
def _get_user_obj():
    """Tenta obter o usuário logado nas APIs novas e legadas do Streamlit."""
    # API nova
    u = getattr(getattr(st, "context", None), "user", None)
    if u:
        return u
    # API legada
    return getattr(st, "user", None)

def get_email() -> str:
    """Extrai o e-mail (ou identificador) do usuário, se houver."""
    u = _get_user_obj()
    if not u:
        return ""
    for attr in ("email", "primaryEmail", "preferred_username"):
        if getattr(u, attr, None):
            return str(getattr(u, attr))
    # fallback: se o objeto suportar str()
    try:
        s = str(u).strip()
        if "@" in s:
            return s
    except Exception:
        pass
    return ""

def check_oidc_secrets() -> Tuple[bool, Dict[str, str]]:
    """Valida se os segredos OIDC essenciais existem antes de chamar st.login."""
    missing = {}
    try:
        cfg = st.secrets["oidc"]
    except Exception:
        return False, {"__section__": "[oidc] não encontrado em secrets"}
    required = ("client_id", "client_secret", "redirect_uri", "discovery_url", "cookie_secret")
    for key in required:
        if not cfg.get(key):
            missing[key] = "faltando"
    return (len(missing) == 0), missing

def ensure_login(provider: str = "oidc"):
    """Chama st.login SOMENTE na página de login, e só se segredos estiverem ok."""
    ok, missing = check_oidc_secrets()
    if not ok:
        st.error("Login Google (OIDC) indisponível: faltam itens em `[oidc]` nos *secrets* da Cloud.")
        with st.expander("Ver itens faltando"):
            st.write(missing)
            st.markdown(
                """
                **Checklist essencial (preencher nos *Secrets* da Streamlit Cloud):**
                ```toml
                [oidc]
                client_id     = "..."
                client_secret = "..."
                redirect_uri  = "https://SEU-APP.streamlit.app/oauth2callback"
                discovery_url = "https://accounts.google.com/.well-known/openid-configuration"
                cookie_secret = "um-segredo-longo-e-estável"
                ```
                """
            )
        st.stop()

    # Somente aqui chamamos st.login(); outras páginas NUNCA chamam.
    if not get_email():
        st.login(provider)  # dispara o fluxo OIDC e faz rerun
        st.stop()

# --------------------------- Página --------------------------------
def main():
    st.title("🔐 Portal Unificado – Login")

    # Garante segredos e chama login apenas aqui
    ensure_login("oidc")

    # Se chegou aqui, usuário está autenticado
    email = get_email()
    st.success(f"Você entrou como **{email}**.")

    # Evita loops de redirecionamento: só redireciona uma vez
    if not st.session_state.get("_redirected_once"):
        st.session_state["_redirected_once"] = True

        # ✅ Redireciona automaticamente para a página de aplicativos
        try:
            st.switch_page("pages/02_Aplicativos-3.py")
        except Exception:
            # Em versões antigas ou se o caminho mudar, mostramos um link seguro
            st.info("Redirecionamento automático indisponível nesta versão. Use o link abaixo:")
            st.page_link("pages/02_Aplicativos-3.py", label="➡️ Ir para Aplicativos", icon=":material/apps:")
    else:
        # Em reruns subsequentes, só ofereça o link (evita ping-pong)
        st.page_link("pages/02_Aplicativos-3.py", label="➡️ Ir para Aplicativos", icon=":material/apps:")

    # Opcional: bloco de diagnóstico rápido (útil enquanto ajusta)
    with st.expander("🔧 Diagnóstico (opcional)"):
        ok, missing = check_oidc_secrets()
        st.write({
            "logged_in_email": email or None,
            "oidc_secrets_ok": ok,
            "missing_keys": list(missing.keys()) if not ok else [],
        })
        if ok:
            # Não mostramos client_secret/cookie_secret por segurança
            try:
                cfg = st.secrets["oidc"]
                st.write({"redirect_uri": cfg.get("redirect_uri"), "discovery_url": cfg.get("discovery_url")})
            except Exception:
                pass

if __name__ == "__main__":
    main()

