import streamlit as st
import random

st.set_page_config(page_title="Spy Game", layout="centered")
st.title("🕵️ Spy Game")

# --- SESSION STATE INIT: ALLT DEFINIERAS HÄR ---
if "step" not in st.session_state:
    st.session_state.step = "setup"
if "players" not in st.session_state:
    st.session_state.players = []
if "num_players" not in st.session_state:
    st.session_state.num_players = 3
if "word_list" not in st.session_state:
    # Inbyggd lista Göteborgsord
    st.session_state.word_list = [
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
if "assignments" not in st.session_state:
    st.session_state.assignments = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "reveal_order" not in st.session_state:
    st.session_state.reveal_order = []
if "show_role" not in st.session_state:
    st.session_state.show_role = False

# --- STEP 1: Setup ---
if st.session_state.step == "setup":
    st.subheader("1. Add Words (leave empty to use default Göteborgsord)")
    word_input = st.text_area("Enter one word per line", height=200)
    if word_input.strip():
        words = [w.strip() for w in word_input.split("\n") if w.strip()]
    else:
        words = st.session_state.word_list

    st.subheader("2. Enter Player Names")
    st.session_state.num_players = st.number_input(
        "Number of players", min_value=3, step=1, value=st.session_state.num_players
    )
    player_names = []
    for i in range(int(st.session_state.num_players)):
        default_name = st.session_state.players[i] if i < len(st.session_state.players) else ""
        name = st.text_input(f"Player {i+1} name", value=default_name)
        player_names.append(name)

    if st.button("Start Game"):
        if len(words) == 0:
            st.error("Please enter at least one word or leave empty to use default list.")
        elif "" in player_names:
            st.error("Please fill in all player names.")
        else:
            st.session_state.word_list = words
            st.session_state.players = player_names

            # Välj ord och spion
            chosen_word = random.choice(words)
            spy_index = random.randint(0, len(player_names) - 1)

            # Tilldela roller
            st.session_state.assignments = [
                "Spy" if i == spy_index else chosen_word for i in range(len(player_names))
            ]

            # Skapa slumpad ordning för vem som börjar se sin roll
            st.session_state.reveal_order = list(range(len(player_names)))
            random.shuffle(st.session_state.reveal_order)

            st.session_state.step = "reveal"
            st.session_state.current_index = 0
            st.session_state.show_role = False
            st.experimental_rerun()

# --- STEP 2: Reveal roles ---
elif st.session_state.step == "reveal":
    current = st.session_state.current_index

    if current >= len(st.session_state.players):
        st.success("✅ All players have viewed their roles.")
        if st.button("🔁 Restart Game"):
            # Behåll namn och antal spelare, nollställ bara spelomgångsdata
            for key in ["assignments", "current_index", "reveal_order", "show_role", "step"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.step = "setup"
            st.experimental_rerun()
        st.stop()

    player_index = st.session_state.reveal_order[current]
    st.subheader("Reveal Player Role")
    st.write(f"Player: **{st.session_state.players[player_index]}**")

    if not st.session_state.show_role:
        if st.button("Reveal Role"):
            st.session_state.show_role = True
    else:
        role = st.session_state.assignments[player_index]
        if role == "Spy":
            st.error("🕵️ You are the SPY!")
        else:
            st.success(f"Your word is: **{role}**")

        if st.button("Next Player"):
            st.session_state.current_index += 1
            st.session_state.show_role = False
            st.experimental_rerun()
