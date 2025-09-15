import streamlit as st

st.set_page_config(page_title="Portal Unificado – Aplicativos", layout="wide", initial_sidebar_state="expanded")

# --------- Utils mínimos ----------
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

def go_to_login():
    for target in ("app.py", "app-8.py", "Home.py", "main.py", "Main.py"):
        try:
            st.switch_page(target)
            return
        except Exception:
            continue
    st.info("Abra a página de **login** pelo menu lateral (ícone '>').")

def guard():
    if not user_email():
        st.warning("Você precisa fazer login na página principal.")
        if st.button("⬅️ Voltar para Login", use_container_width=True):
            go_to_login()
        st.stop()

# --------- UI ----------
def app_card(title: str, desc: str, href: str = "", internal_page: str = "", key: str = ""):
    with st.container(border=True):
        st.subheader(title)
        st.caption(desc)
        col1, col2 = st.columns([1, 3], vertical_alignment="center")
        with col1:
            if internal_page:
                try:
                    st.page_link(internal_page, label="Abrir", icon=":material/open_in_new:")
                except Exception:
                    if st.button("Abrir", use_container_width=True, key=f"open_{key}"):
                        try:
                            st.switch_page(internal_page)
                        except Exception:
                            st.warning("Não foi possível abrir a página interna; verifique o nome do arquivo.")
            elif href:
                st.link_button("Abrir", href, use_container_width=True, key=f"link_{key}")
            else:
                st.button("Indisponível", disabled=True, use_container_width=True, key=f"off_{key}")
        with col2:
            st.write("")

def main():
    guard()
    st.title("🚀 Meus Aplicativos")
    st.caption("Selecione um aplicativo abaixo.")

    apps = [
        {"title":"TG/ADT Events","desc":"Análise de eventos (TG/ADT) e extração de parâmetros.","href":"https://apptgadtgeventspy-hqeqt7yljzwra3r7nmdhju.streamlit.app/"},
        {"title":"Stack Graph","desc":"Gráficos empilhados para dados multidimensionais.","href":"https://appstackgraphpy-ijew8pyut2jkc4x4pa7nbv.streamlit.app/"},
        {"title":"Rheology App","desc":"Análise de reologia e ajuste de modelos.","href":"https://apprheologyapppy-mbkr3wmbdb76t3ysvlfecr.streamlit.app/"},
        {"title":"Mechanical Properties","desc":"Propriedades mecânicas e curvas tensão–deformação.","href":"https://appmechanicalpropertiespy-79l8dejt9kfmmafantscut.streamlit.app/"},
        {"title":"Baseline Smoothing","desc":"Suavização e correção de linha de base em sinais.","href":"https://appbaselinesmoothinglineplotpy-mvx5cnwr5szg4ghwpbx379.streamlit.app/"},
        {"title":"Isotherms App","desc":"Isotermas de adsorção (vários modelos).","href":"https://isothermsappfixedpy-ropmkqgbbxujhvkd6pfxgi.streamlit.app/"},
        {"title":"Histograms","desc":"Geração e análise de histogramas.","href":"https://apphistogramspy-b3kfy7atbdhgxx8udeduma.streamlit.app/"},
        {"title":"Column 3D Line","desc":"Coluna 3D com linha sobreposta.","href":"https://column3dpyline2inmoduleimportdash-kdqhfwwyyhdtb48x4z3kkn.streamlit.app/"},
        {"title":"Crystallinity DSC/XRD","desc":"Cristalinidade por DSC/XRD.","href":"https://appcrystallinitydscxrdpy-wqtymsdcco2nuem7fv3hve.streamlit.app/"},
        {"title":"Column 3D","desc":"Gráficos de barras em 3D (colunas).","href":"https://column3dpy-cskafquxluvyv23hbnhxli.streamlit.app/"},
        {"title":"Kinetic Models","desc":"Modelagem cinética com múltiplos modelos.","href":"https://kineticmodelsapppy-fz8qyt64fahje5acofqpcm.streamlit.app/"},
        {"title":"Python Launcher","desc":"Launcher utilitário para scripts Python.","href":"https://pythonlauncherfixedpy-yschqh6qwzl526xurdeoca.streamlit.app/"},
    ]

    cols = st.columns(3)
    for i, app in enumerate(apps):
        with cols[i % 3]:
            app_card(app["title"], app["desc"], href=app.get("href",""), internal_page=app.get("internal_page",""), key=str(i))

    st.divider()
    if st.button("⬅️ Voltar ao Login", use_container_width=True):
        go_to_login()

if __name__ == "__main__":
    main()





