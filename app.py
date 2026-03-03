import streamlit as st
import google.generativeai as genai

# 1. Configuration
st.set_page_config(page_title="SEO Strategist Pro", page_icon="📊")

with st.sidebar:
    st.title("⚙️ Configuration")
    api_key = st.text_input("Clé API Gemini", type="password")

st.title("📊 SEO Strategist Pro")

# 2. Champs
profession = st.text_input("Profession (ex: Plombier)")
city = st.text_input("Ville (ex: Saint-Maxime)")

if st.button("Lancer l'analyse"):
    if not api_key:
        st.error("Veuillez entrer votre clé API.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # CHANGEMENT MAJEUR ICI : 
            # On utilise 'gemini-1.5-flash-latest' qui est l'alias le plus stable
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
            with st.spinner("Analyse en cours..."):
                # On demande à l'IA de faire sa recherche interne 
                # (Certaines clés API gratuites bloquent l'outil 'tools', 
                # donc on passe par un prompt direct plus puissant)
                prompt = f"""
                Tu es un expert SEO. Fais une recherche en temps réel sur Google pour '{profession} à {city}'. 
                Donne-moi le TOP 5 des résultats, analyse leurs points forts et propose une stratégie SEO locale pour passer devant eux. 
                Réponds en Français de manière très structurée.
                """
                
                response = model.generate_content(prompt)
                
                st.success("Analyse terminée !")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Erreur : {e}")
