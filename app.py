import streamlit as st
from google import genai
from google.genai import types
import os

# Configuration de la page
st.set_page_config(page_title="SEO Strategist Pro", page_icon="📊", layout="wide")

# Style CSS personnalisé
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; background-color: #059669; color: white; border-radius: 10px; }
    .report-container { background-color: white; padding: 30px; border-radius: 20px; border: 1px solid #e5e5e5; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar pour la configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    api_key = st.text_input("Clé API Gemini", type="password")
    st.info("Obtenez votre clé sur [Google AI Studio](https://aistudio.google.com/)")

st.title("📊 SEO Strategist Pro")
st.subheader("Générez une stratégie SEO basée sur l'analyse réelle de la SERP")

# Formulaire d'entrée
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        profession = st.text_input("Profession / Secteur", placeholder="ex: Plombier")
        target = st.text_input("Cible de l'entreprise", placeholder="ex: Particuliers")
    with col2:
        city = st.text_input("Ville / Zone", placeholder="ex: Paris")
        goal = st.selectbox("Objectif du site", [
            "Demande de devis", 
            "Prise de contact / Appel", 
            "Achat en ligne", 
            "Prise de rendez-vous"
        ])

if st.button("Lancer l'analyse stratégique"):
    if not api_key:
        st.error("Veuillez entrer votre clé API Gemini dans la barre latérale.")
    elif not profession or not city:
        st.error("Veuillez remplir au moins la profession et la ville.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            with st.spinner("Analyse de la SERP Google en cours..."):
                prompt = f"""
                Agis en tant qu'expert SEO senior. Analyse la SERP Google pour la requête : "{profession} à {city}".
                
                Contexte :
                - Profession : {profession}
                - Ville : {city}
                - Cible : {target}
                - Objectif : {goal}

                Génère un rapport structuré :
                1. Analyse du Top 5 (Concurrents)
                2. Estimation du volume de recherche mensuel
                3. Stratégie de mots-clés
                4. Note de difficulté SEO (0 à 10) avec justification
                5. Plan d'action concret
                
                Utilise l'outil Google Search pour des données réelles. Réponds en Français.
                """

                # Appel à l'API Gemini avec Google Search
                response = client.models.generate_content(
                    model = client.models.generate_content(
    model="gemini-1.5-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearchRetrieval())]
    )
)

                # Affichage des résultats
                st.success("Analyse terminée !")
                
                # Layout du rapport
                st.markdown("---")
                
                # Affichage du contenu principal
                st.markdown(response.text)

                # Affichage des sources (Grounding)
                if response.candidates[0].grounding_metadata.grounding_chunks:
                    with st.expander("🔗 Sources et références analysées"):
                        for chunk in response.candidates[0].grounding_metadata.grounding_chunks:
                            if chunk.web:
                                st.write(f"- [{chunk.web.title}]({chunk.web.uri})")

        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")

# Footer
st.markdown("---")
st.caption("Propulsé par Google Gemini 2.0 & Streamlit")
