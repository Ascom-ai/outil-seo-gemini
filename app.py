import streamlit as st
from google import genai
from google.genai import types
import os

# Configuration de la page
st.set_page_config(page_title="SEO Strategist Pro", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; background-color: #059669; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("⚙️ Configuration")
    api_key = st.text_input("Clé API Gemini", type="password")
    st.info("Obtenez votre clé sur [Google AI Studio](https://aistudio.google.com/)")

st.title("📊 SEO Strategist Pro")
st.subheader("Analyse réelle de la SERP via Gemini")

col1, col2 = st.columns(2)
with col1:
    profession = st.text_input("Profession", placeholder="ex: Plombier")
    target = st.text_input("Cible", placeholder="ex: Particuliers")
with col2:
    city = st.text_input("Ville", placeholder="ex: Saint-Maxime")
    goal = st.selectbox("Objectif", ["Devis", "Contact", "RDV"])

if st.button("Lancer l'analyse"):
    if not api_key:
        st.error("Entre ta clé API !")
    else:
        try:
            # INITIALISATION CORRECTE POUR LE SDK 2.0
            client = genai.Client(api_key=api_key)
            
            with st.spinner("Recherche Google en cours..."):
                prompt = f"Analyse SEO pour {profession} à {city}. Cible: {target}. Objectif: {goal}. Donne le top 5 et une stratégie."

                # LE CORRECTIF EST ICI : Pas de 'models/' devant le nom
                response = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(google_search=types.GoogleSearchRetrieval())]
                    )
                )

                st.success("Analyse terminée !")
                st.markdown("---")
                st.markdown(response.text)

        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")
