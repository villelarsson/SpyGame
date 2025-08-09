import streamlit as st
import random

st.set_page_config(page_title="Spy Game", layout="centered")
st.title("🕵️ Spy Game")

# --- Inbakad ordlista med Göteborgs-relaterade och andra ord ---
default_words = [
    "Skansen Kronan", "Feskekôrka", "Avenyn", "Liseberg", "Göta älv",
    "Haga", "Kungsportsplatsen", "Slottsskogen", "Majorna", "Järntorget",
    "Ullevi", "Barken Viking", "Älvsborgsbron", "Stenpiren", "Vinga fyr",
    "Operan", "Masthuggskyrkan", "Göteborgs Konstmuseum", "Kvarnberget",
    "Nordstan", "Paddan", "Kungshöjd", "Eriksberg", "Röda Sten",
    "Kungälv", "Bohuslän", "Marstrand", "Göteborgs universitet",
    "Torslanda", "Delsjön", "Gamlestaden", "Frihamnen", "Vasa",
    "Spårvagn", "Trädgårdsföreningen", "Bohusbanan", "Göta kanal",
    "Vasaparken", "Sahlgrenska", "Bergsjön", "Östra Sjukhuset",
    "Kviberg", "Älvsborgs fästning", "Kungsgatan", "Södra Vägen",
    "Chalmers", "Göta älvbron", "Brunnsparken", "Västra Frölunda",
    "Skärgården", "Linné", "Kungstorget"
]

# --- SESSION STATE INIT ---
if "step" not in st.session_state:
    st.session_state.step = "setup"
if "players" not in st.session_state:
    st.session_state.players = []
if "num_players" not in st.session_state:
    st.session_state.num_players = 3
if "word_list" not in st.session_state:
    st.session_state.word_list = default_words
if "assignments" not in st.session_state:
    st.session_state.assignmen_
