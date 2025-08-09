import streamlit as st
import random

st.set_page_config(page_title="Spy Game", layout="centered")
st.title("🕵️ Spy Game")

# Hårdkodad ordlista (Göteborgs ord)
word_list = [
    "Sqwaren", "Bridge", "Linnsparken", "Gullmaren", "GoTento", "Gamtorget",
    "Chalmers", "Fiskekortet", "Mastvindmarknaden", "Molinertwron", "Fiskbatang",
    "Fisketwragen", "Liseberg", "Storagatan", "Marktall", "Slottsskogen",
    "Frolindgen", "Kafebarken", "Valgravern", "Saluhall badmint", "Majorvegen",
    "Kramerros", "Skivbacken", "Eldstalt", "Operahen", "Golemille", "Kontrkyn",
    "Slottsskirkang", "Fisketpanna", "Avenkyrok", "Torslands", "stranda",
    "Garden of ediles", "Slott-channel", "Nordic shipyard", "Kollestalt",
    "Styrsoe", "Stickgort board", "Gatungeran", "Marktscener", "Halstahal gata",
    "Skagen vic"
]

# --- SESSION STATE ---
if "step" not in st.session_state:
    st.session_state.step = "setup"
if "players" not in st.session_state:
    st.session_state.players = []
if "num_players" not in st.session_state:
    st.session_state.num_players = 3
if "assignments" not in st.session_state:
    st.session_state.assignments = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "reveal_order" not in st.session_state:
    st.session_state.reveal_order = []
if "show_role" not in st.session_state:
    st.session_state.show_role = False

def start_game():
    chosen_word = random.choice(word_list)
    spy_index = random.randint(0, len(st.session_state.players) - 1)
    st.session_state.assignments = [
        "Spy" if i == spy_index else chosen_word for i in range(len(st.session_state.players))
    ]
    st.session_state.reveal_order = list(range(len(st.session_state.players)))
    random.shuffle(st.session_state.reveal_order)
    st.session_state.step = "reveal"
    st.session_state.current_index = 0
    st.session_state.show_role = False

def next_player():
    st.session_state.current_index += 1
    st.session_state.show_role = False

def restart_game():
    # Behåll spelare och antal, nollställ allt annat
    for key in ["assignments", "current_index", "reveal_order", "show_role", "step"]:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.step = "setup"

# --- Setup step ---
if st.session_state.step == "setup":
    st.subheader("Enter Player Names")
    st.session_state.num_players = st.number_input("Number of players", min_value=3, step=1, value=st.session_state.num_players)
    player_names = []
    for i in range(st.session_state.num_players):
        default_name = st.session_state.players[i] if i < len(st.session_state.players) else ""
        name = st.text_input(f"Player {i+1} name", value=default_name)
        player_names.append(name)

    if st.button("Start Game"):
        if "" in player_names:
            st.error("Please fill in all player names.")
        else:
            st.session_state.players = player_names
            start_game()

# --- Reveal step ---
elif st.session_state.step == "reveal":
    if st.session_state.current_index >= len(st.session_state.players):
        st.success("✅ All players have viewed their roles.")
        if st.button("Restart Game", on_click=restart_game):
            pass
    else:
        player_idx = st.session_state.reveal_order[st.session_state.current_index]
        st.subheader("Reveal Player Role")
        st.write(f"Player: **{st.session_state.players[player_idx]}**")

        if not st.session_state.show_role:
            if st.button("Reveal Role"):
                st.session_state.show_role = True
        else:
            role = st.session_state.assignments[player_idx]
            if role == "Spy":
                st.error("🕵️ You are the SPY!")
            else:
                st.success(f"Your word is: **{role}**")
            st.button("Next Player", on_click=next_player)
