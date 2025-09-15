import streamlit as st
from typing import Dict, Tuple, Optional

st.set_page_config(
    page_title="Portal Unificado – Login",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------- Utils de usuário -------------------
def _get_user_obj():
    u = getattr(getattr(st, "context", None), "user", None)
    return u if u else getattr(st, "user", None)

def get_email() -> str:
    u = _get_user_obj()
    if not u:
        return ""
    for attr in ("email", "primaryEmail", "preferred_username"):
        if getattr(u, attr, None):
            return str(getattr(u, attr))
    try:
        s = str(u).strip()
        if "@" in s:
            return s
    except Exception:
        pass
    return ""

# ------------------- Detecta provedor e valida secrets -------------------
def _dict_get(d: Dict, *path, default=None):
    cur = d
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur

def detect_provider_and_validate() -> Tuple[Optional[str], bool, Dict[str, str]]:
    """
    Retorna (provider, ok, missing):
      - provider: "google" | "oidc" | None
      - ok: se tem o mínimo para tentar logar
      - missing: chaves faltantes (para debug)
    """
    missing = {}

    # 1) Preferir auth.google
    auth = dict(st.secrets).get("auth", {})
    google = auth.get("google", {})
    # Requisitos mínimos para google: client_id e client_secret
    g_missing = {k: "faltando" for k in ("client_id", "client_secret") if not google.get(k)}
    if not g_missing:
        # Opcional: cookie_secret em [auth]
        cookie_secret = auth.get("cookie_secret")
        # Não bloqueia se faltar, apenas sinaliza
        if not cookie_secret:
            g_missing["(opcional) auth.cookie_secret"] = "recomendado (token longo e estável)"
        return "google", True, g_missing

    # 2) Fallback: oidc "genérico"
    oidc = dict(st.secrets).get("oidc", {})
    o_required = ("client_id", "client_secret", "redirect_uri", "discovery_url", "cookie_secret")
    o_missing = {k: "faltando" for k in o_required if not oidc.get(k)}
    if not o_missing:
        return "oidc", True, {}

    # Nenhum provedor completo encontrado → reportar faltas
    if google or auth:  # tinha [auth] mas incompleto
        return None, False, {"[auth.google]": g_missing or "faltando seção", "(sugestão)": "preencher client_id e client_secret"}
    if oidc:  # tinha [oidc] mas incompleto
        return None, False, {"[oidc]": o_missing}
    return None, False, {"__section__": "Nenhuma seção de auth encontrada. Use [auth.google] OU [oidc]."}

def ensure_login():
    provider, ok, missing = detect_provider_and_validate()
    if not ok or provider is None:
        st.error("Login indisponível: verifique as credenciais de autenticação nos *Secrets*.")
        with st.expander("Ver itens faltando"):
            st.write(missing)
            st.markdown(
                """
**Modelos válidos de configuração (preencher em `Secrets` da Streamlit Cloud):**

**Opção A – Google (recomendada):**
```toml
[auth]
cookie_secret = "um-token-bem-longo-e-estavel"  # opcional, mas recomendado

[auth.google]
client_id     = "SEU_CLIENT_ID"
client_secret = "SEU_CLIENT_SECRET"
# redirect_uri (normalmente a Cloud cuida disso; se precisar, use):
# redirect_uri  = "https://SEU-APP.streamlit.app/oauth2callback"



