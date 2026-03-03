import streamlit as st
from google import genai
from google.genai import types
import os

# 1. Configuration de la page
st.set_page_config(page_title="SEO Strategist Pro", page_icon="📊", layout="wide")

# 2. Style CSS pour une interface propre
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { 
        width: 100%; 
        background-color: #059669; 
        color: white; 
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    .report-container { 
        background-color: white; 
        padding: 20px; 
        border-radius: 15px; 
        border: 1px solid #e5e5e5; 
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Barre latérale pour la clé API
with st.sidebar:
    st.title("⚙️ Configuration")
    api_key = st.text_input("Clé API Gemini", type="password")
    st.info("Récupérez votre clé sur [Google AI Studio](https://aistudio.google.com/)")

# 4. En-tête principal
st.title("📊 SEO Strategist Pro")
st.subheader("Analyse de la SERP réelle et Stratégie SEO Locale")

# 5. Formulaire de saisie
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        profession = st.text_input("Profession / Secteur", placeholder="ex: Plombier")
        target = st.text_input("Cible de l'entreprise", placeholder="ex: Particuliers locaux")
    with col2:
        city = st.text_input("Ville / Zone de chalandise", placeholder="ex: Saint-Maxime")
        goal = st.selectbox("Objectif principal", [
            "Demande de devis", 
            "Appel téléphonique", 
            "Vente en ligne", 
            "Prise de rendez-vous"
        ])

# 6. Logique d'analyse
if st.button("Lancer l'analyse stratégique"):
    if not api_key:
        st.error("❌ Veuillez entrer votre clé API Gemini dans la barre latérale.")
    elif not profession or not city:
        st.error("⚠️ Veuillez remplir au moins les champs 'Profession' et 'Ville'.")
    else:
        try:
            # Initialisation du client avec le nouveau SDK google-genai
            client = genai.Client(api_key=api_key)
            
            with st.spinner(f"Analyse en cours pour {profession} à {city}..."):
                
                # Construction du prompt expert
                prompt = f"""
                Agis en tant qu'expert SEO senior spécialisé en référencement local. 
                Analyse la SERP Google réelle pour la requête : "{profession} à {city}".
                
                Données de contexte :
                - Métier : {profession}
                - Localisation : {city}
                - Audience cible : {target}
                - Conversion attendue : {goal}

                Fournis un rapport détaillé comprenant :
                1. Analyse des 5 premiers concurrents (Titres et angles marketing).
                2. Intention de recherche dominante.
                3. Top 10 des mots-clés sémantiques à intégrer.
                4. Structure recommandée pour la page d'accueil (H1, H2, H3).
                5. Conseils spécifiques pour surpasser les concurrents actuels.
                
                Utilise l'outil de recherche Google. Réponds de manière structurée en Français.
                """

                # APPEL API CORRIGÉ POUR ÉVITER LA 404
                # Note : On n'utilise PAS le préfixe 'models/' ici
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(google_search=types.GoogleSearchRetrieval())]
                    )
                )

                # 7. Affichage des résultats
                st.success("✅ Analyse terminée avec succès !")
                st.markdown("---")
                
                # Affichage du rapport SEO
                st.markdown(response.text)

                # Affichage des sources (Grounding)
                try:
                    if response.candidates[0].grounding_metadata:
                        with st.expander("🔗 Voir les sources de la recherche Google"):
                            st.write("L'IA a scanné les résultats actuels pour produire ce rapport.")
                except:
                    pass

        except Exception as e:
            # Gestion simplifiée des erreurs de quota ou autres
            if "429" in str(e):
                st.error("⏳ Quota dépassé. Veuillez patienter une minute avant de réessayer.")
            else:
                st.error(f"❌ Une erreur est survenue : {e}")

# Footer
st.markdown("---")
st.caption("Outil de veille SEO - Propulsé par Google Gemini 1.5 Flash")
