import streamlit as st
import google.generativeai as genai

# 1. Configuration de la page
st.set_page_config(page_title="SEO Strategist Pro", page_icon="📊", layout="wide")

# 2. Sidebar pour la Clé API
with st.sidebar:
    st.title("⚙️ Configuration")
    api_key = st.text_input("Clé API Gemini", type="password")
    st.info("Clé disponible sur [Google AI Studio](https://aistudio.google.com/)")

# 3. Interface principale
st.title("📊 SEO Strategist Pro")
st.subheader("Analyse de la SERP en temps réel")

col1, col2 = st.columns(2)
with col1:
    profession = st.text_input("Profession", placeholder="ex: Plombier")
    city = st.text_input("Ville", placeholder="ex: Saint-Maxime")
with col2:
    target = st.text_input("Cible", placeholder="ex: Particuliers")
    goal = st.selectbox("Objectif", ["Devis", "Appel", "RDV"])

# 4. Logique d'exécution
if st.button("Lancer l'analyse stratégique"):
    if not api_key:
        st.error("Veuillez entrer votre clé API.")
    elif not profession or not city:
        st.error("Veuillez remplir les champs Profession et Ville.")
    else:
        try:
            # Configuration de la bibliothèque
            genai.configure(api_key=api_key)
            
            # SYNTAXE CORRIGÉE POUR L'OUTIL SEARCH
            # On utilise 'google_search_retrieval' au lieu de 'google_search'
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                tools=[{'google_search_retrieval': {}}]
            )
            
            with st.spinner(f"Recherche Google en direct pour {profession} à {city}..."):
                prompt = f"Expert SEO : Analyse la SERP pour '{profession} à {city}'. Donne le top 5, les points forts des concurrents et une stratégie SEO pour l'objectif '{goal}' en Français."
                
                # Appel à l'API
                response = model.generate_content(prompt)
                
                st.success("Analyse terminée !")
                st.markdown("---")
                
                # Affichage du résultat
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Détails de l'erreur : {e}")

# Footer
st.markdown("---")
st.caption("Propulsé par Google Gemini 1.5 Flash")
