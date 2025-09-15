import streamlit as st

st.set_page_config(
    page_title="Portal Unificado – Aplicativos",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------ Utilitários mínimos (sem chamar st.login aqui!) ------------
def _get_user_obj():
    u = getattr(getattr(st, "context", None), "user", None)
    if u:
        return u
    return getattr(st, "user", None)

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

def stop_if_not_logged():
    # 👉 NUNCA chame st.login aqui; só bloqueie e oriente a voltar ao login
    if not get_email():
        st.warning("Você precisa fazer login na página principal.")
        st.page_link("app-8.py", label="⬅️ Voltar para Login", icon=":material/login:")
        st.stop()

# --------------------------- Página --------------------------------------
def app_card(title: str, description: str, href: str = "", internal_page: str = ""):
    """Cartão simples para listar apps. Use href para externo ou internal_page para páginas internas."""
    with st.container(border=True):
        st.subheader(title)
        st.caption(description)
        col1, col2 = st.columns([1, 3], vertical_alignment="center")

        with col1:
            if internal_page:
                st.page_link(internal_page, label="Abrir", icon=":material/open_in_new:")
            elif href:
                st.link_button("Abrir", href, use_container_width=True)
            else:
                st.button("Indisponível", disabled=True, use_container_width=True)

        with col2:
            st.write("")  # espaço para futuro: tags, badges, etc.

def main():
    stop_if_not_logged()  # garante que só usuários autenticados vejam esta página

    st.title("🚀 Meus Aplicativos")
    st.caption("Selecione um aplicativo abaixo.")

    # ======== TODOS OS LINKS INCLUÍDOS ========
    apps = [
        {
            "title": "TG/ADT Events",
            "desc": "Análise de eventos (TG/ADT) e extração de parâmetros.",
            "href": "https://apptgadtgeventspy-hqeqt7yljzwra3r7nmdhju.streamlit.app/",
            "internal_page": "",
        },
        {
            "title": "Stack Graph",
            "desc": "Gráficos empilhados para dados multidimensionais.",
            "href": "https://appstackgraphpy-ijew8pyut2jkc4x4pa7nbv.streamlit.app/",
            "internal_page": "",
        },
        {
            "title": "Rheology App",
            "desc": "Análise de reologia e ajuste de modelos.",
            "href": "https://apprheologyapppy-mbkr3wmbdb76t3ysvlfecr.streamlit.app/",
            "internal_page": "",
        },
        {
            "title": "Mechanical Properties",
            "desc": "Propriedades mecânicas e curvas tensão–deformação.",
            "href": "https://appmechanicalpropertiespy-79l8dejt9kfmmafantscut.streamlit.app/",
            "internal_page": "",
        },
        {
            "title": "Baseline Smoothing",
            "desc": "Suavização e correção de linha de base em sinais.",
            "href": "https://appbaselinesmoothinglineplotpy-mvx5cnwr5szg4ghwpbx379.streamlit.app/",
            "internal_page": "",
        },
        {
            "title": "Isotherms App",
            "desc": "Ajuste de isotermas de adsorção (vários modelos).",
            "href": "https://isothermsappfixedpy-ropmkqgbbxujhvkd6pfxgi.streamlit.app/",
            "internal_page": "",
        },
        {
            "title": "Histograms",
            "desc": "Geração e análise de histogramas.",
            "href": "https://apphistogramspy-b3kfy7atbdhgxx8udeduma.streamlit.app/",
            "internal_page": "",
        },
        {
            "title": "Column 3D Line",
            "desc": "Visualização tipo coluna 3D com linha sobreposta.",
            "href": "https://column3dpyline2inmoduleimportdash-kdqhfwwyyhdtb48x4z3kkn.streamlit.app/",
            "internal_page": "",
        },
        {
            "title": "Crystallinity DSC/XRD",
            "desc": "Cristalinidade por DSC/XRD com utilidades de cálculo.",
            "href": "https://appcrystallinitydscxrdpy-wqtymsdcco2nuem7fv3hve.streamlit.app/",
            "internal_page": "",
        },
        {
            "title": "Column 3D",
            "desc": "Gráficos de barras em 3D (colunas).",
            "href": "https://column3dpy-cskafquxluvyv23hbnhxli.streamlit.app/",
            "internal_page": "",
        },
        {
            "title": "Kinetic Models",
            "desc": "Modelagem cinética com múltiplos modelos.",
            "href": "https://kineticmodelsapppy-fz8qyt64fahje5acofqpcm.streamlit.app/",
            "internal_page": "",
        },
        {
            "title": "Python Launcher",
            "desc": "Launcher utilitário para scripts Python.",
            "href": "https://pythonlauncherfixedpy-yschqh6qwzl526xurdeoca.streamlit.app/",
            "internal_page": "",
        },
    ]
    # ===========================================

    # Grid responsivo simples
    cols = st.columns(3)
    for i, app in enumerate(apps):
        with cols[i % 3]:
            app_card(
                title=app["title"],
                description=app["desc"],
                href=app.get("href", ""),
                internal_page=app.get("internal_page", ""),
            )

    st.divider()
    st.page_link("app-8.py", label="⬅️ Voltar ao Login", icon=":material/login:")

if __name__ == "__main__":
    main()

