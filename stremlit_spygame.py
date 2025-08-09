import streamlit as st
import random

st.set_page_config(page_title="Spy Game", layout="centered")
st.title("🕵️ Spy Game")

# -----------------------
# ORD: Direkt inbakad lista (Göteborg + blandat)
# Lägg till/ändra ord här om du vill
DEFAULT_WORDS = [
    # Göteborgsrelaterat (exempel)
    "Avenyn","Liseberg","Hisingen","Slottskogen","Ullevi","Skansen Kronan","Poseidon","Nordstan",
    "Feskekôrka","Älvsborgsbron","Götaälvbron","Götaplatsen","Linné","Masthugget","Haga","Majorna",
    "Frölunda","Vasastan","Brunnsparken","Korsvägen","Bohuslän","Skärgården","Paddan","Kungsportsplatsen",
    "Saltholmen","Chalmers","Eriksberg","Backaplan","Redbergsplatsen","Järntorget","Långgatorna",
    "Botaniska","Trädgårdsföreningen","Gamlestaden","Kortedala","Angered","Partille","Torslanda","Styrsö",
    "Vrångö","Donsö","Askim","Mölndal","Öckerö","Långedrag","Örgryte","Kungälv","Göteborgsoperan",
    "Röda Sten","Lilla Bommen","Gothia Towers","Skeppsbron","Masthuggskajen",

    # Allmänna substantiv / saker
    "Buss","Träd","Bok","Soffa","Mobil","Glass","Hammock","Fika","Skor","Lampa","Katt","Hatt",
    "Tröja","Snö","Spel","Dator","Tåg","Pennor","Väska","Kudde","Båt","Hus","Flygplan","Gaffel",
    "Bänk","Stol","Klocka","Kamera","Moln","Bokhylla","Fönster","Bröd","Hjul","Cykel","Gata","Bil",
    "Leksak","Telefon","Tavla","Radio","Kylskåp","Sked","Boll","Högtalare","Ljusstake","Flagga",
    "Paraply","Nyckel","Karta","Hjälm","Fyr","Brygga","Skepp","Hamnen","Isbrytare","Kaffemaskin",

    # Mat & dryck
    "Köttbulle","Semla","Sill","Pannkaka","Kanelbulle","Korv med bröd","Kaffe","Julmust","Ostkaka",
    "Surströmming","Smörgås","Prinskorv","Marabou","Äpple","Päron","Mjölk","Knäckebröd","Havregryn",

    # Extra neutrala ord för variation
    "Nyckelknippa","Tändsticka","Fjärrkontroll","Mikrovågsugn","Skrivbord","Notbok","Sax",
    "Plånbok","Kikare","Termos","Fiskebil","Ljuslykta","Kartong","Postlåda","Blyertspenna"
]
# -----------------------

# ---- Session state defaults ----
if "step" not in st.session_state:
    st.session_state.step = "setup"
if "num_players" not in st.session_state:
    st.session_state.num_players = 3
if "players" not in st.session_state:
    st.session_state.players = []          # lista med namn i inmatningsordning
if "assignments" not in st.session_state:
    st.session_state.assignments = []      # lista roll per index (samma längd som players)
if "reveal_order" not in st.session_state:
    st.session_state.reveal_order = []     # lista av indices i slumpad ordning
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "show_role" not in st.session_state:
    st.session_state.show_role = False
if "word_list" not in st.session_state:
    st.session_state.word_list = DEFAULT_WORDS.copy()

# ---------- SETUP (form) ----------
st.subheader("1. Setup")

# Number of players (persistas i session_state)
st.session_state.num_players = st.number_input(
    "Number of players", min_value=3, step=1, value=st.session_state.num_players, key="num_players_input"
)

# Använd form för att samla in alla namn i ett svep (minskar onödiga reruns)
with st.form("setup_form"):
    name_inputs = []
    for i in range(int(st.session_state.num_players)):
        # Förifyll från tidigare namn om de finns
        default_val = st.session_state.players[i] if i < len(st.session_state.players) else ""
        name = st.text_input(f"Player {i+1} name", value=default_val, key=f"name_{i}")
        name_inputs.append(name)

    start = st.form_submit_button("Start Game")

# När formuläret skickas
if start:
    # Läs namn direkt från session_state (säkrare än lokala variabler i vissa fall)
    names = [st.session_state.get(f"name_{i}", "").strip() for i in range(int(st.session_state.num_players))]
    if "" in names:
        st.error("Please fill in all player names.")
    else:
        # Spara spelare i session_state (behåll inmatningsordning här)
        st.session_state.players = names
        # Välj ord och spion
        chosen_word = random.choice(st.session_state.word_list)
        spy_index = random.randrange(len(names))
        # assignments i samma indexordning som players
        st.session_state.assignments = ["Spy" if i == spy_index else chosen_word for i in range(len(names))]

        # Slumpa reveal-ordningen (helt oberoende av inmatningsordningen)
        st.session_state.reveal_order = list(range(len(names)))
        random.shuffle(st.session_state.reveal_order)

        # starta reveal-steget
        st.session_state.current_index = 0
        st.session_state.show_role = False
        st.session_state.step = "reveal"
        st.experimental_rerun()

# ---------- REVEAL ----------
if st.session_state.step == "reveal":
    st.subheader("2. Reveal roles")

    # safety: om ingen players (borde inte hända) -> gå tillbaka
    if not st.session_state.players:
        st.warning("No players found — go back to setup.")
        if st.button("Back to setup"):
            st.session_state.step = "setup"
            st.experimental_rerun()

    current = st.session_state.current_index

    # Alla spelare visade?
    if current >= len(st.session_state.players):
        st.success("✅ All players have viewed their roles.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔁 New round (same players)", key="new_round"):
                # Ny runda med samma spelare: välj nytt ord + spion och slumpar ordningen igen
                chosen_word = random.choice(st.session_state.word_list)
                spy_index = random.randrange(len(st.session_state.players))
                st.session_state.assignments = ["Spy" if i == spy_index else chosen_word for i in range(len(st.session_state.players))]
                st.session_state.reveal_order = list(range(len(st.session_state.players)))
                random.shuffle(st.session_state.reveal_order)
                st.session_state.current_index = 0
                st.session_state.show_role = False
                st.experimental_rerun()
