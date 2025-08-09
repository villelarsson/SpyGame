import streamlit as st
import random
import base64

st.set_page_config(page_title="Spy Game", layout="centered")
st.title("🕵️ Spy Game")

# --- SESSION STATE INIT ---
if "step" not in st.session_state:
    st.session_state.step = "setup"
if "players" not in st.session_state:
    st.session_state.players = []
if "num_players" not in st.session_state:
    st.session_state.num_players = 3
if "word_list" not in st.session_state:
    # Göteborg + extra ord, kodade
    encoded_words = "U3F1YXJlbiBCcmlkZ2UgLExpbnNwYXJrZW4sR3VsbW1hcmVuLEdvVGVudCwgR2FtdG9yZ2V0LENoYWxtZXJzLCBGaXNrZWtvcmtldCxNYXN0dmluZG1hcmtuYWRlbiwgTW9saW5ld3JvbnQsIEZpc2tiYXRhbmcsIEZpc2tld3JhZ2VuLCBMaXNlYmVyZywgU3RvcmFnYXRhbiwgTWFya3RhbGwsIFNsb3R0c2tvZ2VuLCBGcm9saW5kZ2VuLCBLYWZlYmFya2VuLCBHYWxnZXRvcCBwYXJrZW4sIEtvcnZlcmssIFZhbGdyYXZlbiwgU2FsdWhhbGwgYmFkbWludCwgTWFqb3J2ZWdlbiwgS3JhbWVyY3JvcywgU2tpdmJhY2tlbiwgRWxkc3RhbHQsIE9wZXJhaGVuLCBHb2xlbWlsbGUsIEtvbnRya3luLCBTbG90dHNraXJrYW4sIEZpc2tldHBhbm5hLCBBdmVua3lyb2ssIFRvcnNsYW5kcywgc3RyYW5kYSwgR2FyZGVuIG9mIGVkaWxlcywgU2xvdHQtY2hhbm5lbCwgTm9yZGljIHNoaXB5YXJkLEtvbGxlc3RhbHQsIFN0eXJzb2UsIFN0aWNrZ29ydCBib2FyZCwgR2F0dW5nZXJhbiwgTWFya3RzY2VuZXIsIEhhbHN0YWhhbGwgZ2F0YSwgU2thZ2VuIHZpYw=="
    st.session_state.word_list = [w.strip() for w in base64.b64decode(encoded_words).decode("utf-8").split(",")]
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
    st.subheader("1. Enter Player Names")
    st.session_state.num_players = st.number_input("Number of players", min_value=3, step=1, value=st.session_state.num_players)
    
    temp_names = []
    for i in range(int(st.session_state.num_players)):
        default_name = st.session_state.players[i] if i < len(st.session_state.players) else ""
        name = st.text_input(f"Player {i+1} name", value=default_name)
        temp_names.append(name)

    if st.button("Start Game"):
        if "" in temp_names:
            st.error("Please fill in all player names.")
        else:
            st.session_state.players = temp_names

            # Choose word and spy
            chosen_word = random.choice(st.session_state.word_list)
            spy_index = random.randint(0, len(st.session_state.players) - 1)

            # Assign roles
            st.session_state.assignments = [
                "Spy" if i == spy_index else chosen_word for i in range(len(st.session_state.players))
            ]

            # Create random reveal order
            st.session_state.reveal_order = list(range(len(st.session_state.players)))
            random.shuffle(st.session_state.reveal_order)

            st.session_state.step = "reveal"
            st.session_state.current_index = 0
            st.session_state.show_role = False
            st.rerun()

# --- STEP 2: Reveal roles ---
elif st.session_state.step == "reveal":
    current = st.session_state.current_index

    if current >= len(st.session_state.players):
        st.success("✅ All players have viewed their roles.")
        if st.button("🔁 Restart Game"):
            # Reset only game-specific keys, keep players & num_players
            for key in ["assignments", "current_index", "reveal_order", "show_role", "step"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.step = "setup"
            st.rerun()
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
            st.rerun()
