import streamlit as st

def show_sidebar():
    """
    Affiche la barre latérale avec les informations utilisateur et 
    le choix du modèle (OpenAI vs Mistral) avec logos.
    """

    # Afficher les options avec logos pour choisir le modèle
    st.sidebar.title(" 🤖 Choix du modèle")

    # Chargement des images des logos
    openai_logo = "assets/openai_logo.png"
    mistral_logo = "assets/mistral_logo.png"

    col1, col2 = st.sidebar.columns(2)

    with col1:
        st.image(openai_logo, width=100)
        if st.button("Utiliser OpenAI"):
            st.session_state["selected_model"] = "OpenAI"

    with col2:
        st.image(mistral_logo, width=100)
        if st.button("Utiliser Mistral"):
            st.session_state["selected_model"] = "Mistral"

    # Afficher le modèle sélectionné
    selected_model = st.session_state.get("selected_model", "OpenAI")
    st.sidebar.success(f"✅ Modèle sélectionné : {selected_model}")

    return selected_model
