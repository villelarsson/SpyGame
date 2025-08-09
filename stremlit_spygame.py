import streamlit as st
import random

st.set_page_config(page_title="Spy Game", layout="centered")
st.title("🕵️ Spy Game")

# Hårdkodad ordlista (Göteborgs ord)
word_list = [
    "Avenyn", "Linnéplatsen", "Kungsportsplatsen", "Slottsskogen", "Göta älv",
    "Feskekôrka", "Liseberg", "Skansen Kronan", "Masthuggskyrkan", "Nordstan",
    "Chalmers", "Haga", "Röda Sten", "Älvsborgsbron", "Kungsgatan",
    "Göteborgsoperan", "Paddan", "Barken Viking", "Mölndal", "Hisingen",
    "Kviberg", "Majorna", "Västra Frölunda", "Örgryte", "Gamlestaden",
    "Backaplan", "Saltholmen", "Kungsport", "Masthugget", "Eriksberg",
    "Skatås", "Delsjön", "Svenska Mässan", "Ullevi", "Nya Ullevi",
    "Lilla Bommen", "Stora Teatern", "Götaplatsen", "Göteborgs Konstmuseum",
    "Stenpiren", "Kålltorp", "Sannegården", "Bagaregården", "Redbergslid",
    "Olskroken", "Brunnsparken", "Vasa", "Gamla Ullevi", "Pölsehallen",
    "Göteborgs Stadsmuseum", "Heden", "Skandia Teatern", "Vinga", "Kortedala",
    "Tuve", "Länsmansgården", "Röda Sten Konsthall", "Gunnebo Slott",
    "Bohus fästning", "Sven-Harrys Konstmuseum", "Volvo Torslanda",
    "Göteborgs Universitet", "Kronhuset", "Nefertiti", "Masthugget",
    "Mölndalsån", "Göta älvbron", "Kajskjul",
    # Kända göteborgare / legendarer
    "Leif Loket Olsson", "Håkan Hellström", "Zlatan Ibrahimović", "Lotta Schelin",
    "Ingemar Johansson", "Jan Johansson", "Bengt Ekerot", "Gösta Ekman",
    "Peter Forsberg", "Annika Sörenstam", "Gunnar Gren", "Henrik Lundqvist",
    "Lars Winnerbäck", "Greta Garbo", "Torgny Segerstedt", "Alfred Nobel",
    "Anders Celsius",
    # Platser igen
    "Göteborgs Konsthall", "Göteborgs Stadsteater", "Göteborgs Naturhistoriska Museum",
    "Göteborgs Botaniska Trädgård", "Östra Hamngatan", "Södra Vägen", "Götaleden",
    "Järntorget", "Skärgården", "Delsjöområdet", "Slottsberget", "Kvarnberget",
    "Ruddalen", "Långedrag", "Västra Götaland", "Bohuslän", "Styrsö", "Donsö",
    "Vrångö", "Brännö", "Kungälv", "Torslanda", "Säve", "Majvallen",
    "Öckerö", "Hönö", "Vinga fyr", "Skagen", "Göteborgs Centralstation",
    "Nordstan", "Bohus fästning", "Göteborgs Hamn", "Nya Varvet",
    "Älvsborgs fästning", "Göteborgs Rådhus", "Chalmers Tekniska Högskola",
    "Göteborgs stadsbibliotek", "Göteborgs Konserthus", "Karl Johans Torg",
    "Skatås motionscentrum", "Röda Sten Kulturfabrik", "Kviberg",
    "Gamla Ullevi", "Vasaplatsen", "Östra sjukhuset", "Linnéstaden",
    "Guldheden", "Haga Nygata", "Järntorget", "Kvarteret Krukan",
    "Göteborgsvarvet", "Volvo Museum"
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


