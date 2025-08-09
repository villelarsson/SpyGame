import streamlit as st
import random
import base64

st.set_page_config(page_title="Spy Game", layout="centered")

st.title("🕵️ Spy Game")

# --- SESSION STATE ---
if "step" not in st.session_state:
    st.session_state.step = "setup"
if "players" not in st.session_state:
    st.session_state.players = []
if "word_list" not in st.session_state:
    # Decode a base64 hidden Göteborg + misc word list
    hidden_words_b64 = """
U3RvcmFndGFuLCBHb3RlbmJ1cmcsIFNrYW5zZW4sIFBhbmtodXNldCwgTGlzZWJlcmdzZW4sIEZpc2tsZWJhdGVuLCBIYWdhbXluZSwgQm90dGVuc2lhbiwg
U2xvdHRza29nZW4sIEhlbGxzYm9yZywgR2V0ZXJib3JnLCBLdW5nc2JhY2tlbiwgVmFzdHJhIEh1Z2csIFN0ZW5sdCBmYXN0aWdlbiwgUG9zZW4sIEtlbm5l
YnksIEJyb25zIFBhcmsuLi4=
    """
    decoded = base64.b64decode(hidden_words_b64).decode("utf-8")
    st.session_state.word_list = [w.strip() for w in decoded.split(",") if w.strip()]
if "assignments" not in st.session_state:
    st.session_state.assignments = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

# --- STEP 1: Setup ---
if st.session_state.step == "setup":
    st.subheader("1. Player Names")
    num_players = st.number_input("Number of players", min_value=3, step=1)
    player_names = []
    for i in range(int(num_players)):
        name = st.text_input(f"Player {i+1} name")
        player_names.append(name)

    if st.button("Start Game"):
        if "" in player_names:
            st.error("Please fill in all player names.")
        else:
            words = st.session_state.word_list
            chosen_word = random.choice(words)
            spy_index = random.randint(0, len(player_names) - 1)

            # Assign word or "Spy"
            st.session_state.assignments = [
                "Spy" if i == spy_index else chosen_word for i in range(len(player_names))
            ]
            random.shuffle(st.session_state.assignments)  # Randomize viewing order
            random.shuffle(st.session_state.players)      # Randomize player order
            st.session_state.players = player_names
            st.session_state.step = "reveal"
            st.rerun()

# --- STEP 2: Reveal roles ---
elif st.session_state.step == "reveal":
    current = st.session_state.current_index

    if current >= len(st.session_state.players):
        st.success("✅ All players have viewed their roles.")
        if st.button("🔁 Restart Game"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        st.stop()

    st.subheader("Reveal Player Role")
    st.write(f"Player: **{st.session_state.players[current]}**")

    if "show_role" not in st.session_state:
        st.session_state.show_role = False

    if not st.session_state.show_role:
        if st.button("Reveal Role"):
            st.session_state.show_role = True
    else:
        role = st.session_state.assignments[current]
        if role == "Spy":
            st.error("🕵️ You are the SPY!")
        else:
            st.success(f"Your word is: **{role}**")

        if st.button("Next Player"):
            st.session_state.current_index += 1
            st.session_state.show_role = False
            st.rerun()
