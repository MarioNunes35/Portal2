import streamlit as st

st.set_page_config(
    page_title="Portal Unificado – Aplicativos",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------- Utilitários (sem chamar st.login aqui!) --------------
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

def go_to_login():
    """Tenta voltar para a página principal do app com st.switch_page().
       Permite configurar o arquivo principal via secrets: [app] main_file="app-8.py"
    """
    main_file = st.secrets.get("app", {}).get("main_file", "app-8.py")
    candidates = [main_file, "app.py", "Home.py", "main.py", "Main.py"]
    for target in candidates:
        try:
            st.switch_page(target)
            return
        except Exception:
            continue
    # Se nada funcionou, informa o usuário
    st.info("Não foi possível redirecionar automaticamente. Abra a página de **login** pelo menu (ícone “>” no topo).")

def stop_if_not_logged():
    # 👉 NUNCA chame st.login aqui; só bloqueie e ofereça um botão para voltar
    if not get_email():
        st.warning("Você precisa fazer login na página principal para acessar os aplicativos.")
        if st.button("⬅️ Voltar para Login", use_container_width=True):
            go_to_login()
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
                # Para páginas internas deste MESMO projeto, opcional:
                try:
                    st.page_link(internal_page, label="Abrir", icon=":material/open_in_new:")
                except Exception:
                    # Fallback: tenta switch_page
                    if st.button("Abrir", use_container_width=True):
                        try:
                            st.switch_page(internal_page)
                        except Exception:
                            st.warning("Não foi possível abrir a página interna; verifique o nome do arquivo.")
            elif href:
                st.link_button("Abrir", href, use_container_width=True)
            else:
                st.button("Indisponível", disabled=True, use_container_width=True)

        with col2:
            st.write("")  # espaço para tags/badges no futuro

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
    # Em vez de page_link aqui, ofereça o mesmo botão seguro:
    if st.button("⬅️ Voltar ao Login", use_container_width=True):
        go_to_login()

if __name__ == "__main__":
    main()


