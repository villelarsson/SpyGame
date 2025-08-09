import streamlit as st
import random

st.set_page_config(page_title="Spy Game", layout="centered")
st.title("🕵️ Spy Game")

# Hårdkodad ordlista (Göteborgs ord)
word_list = [
    "Avenyn", "Linnéplatsen", "Kungsportsplatsen", "Slottsskogen", "Göta älv",
    "Feskekôrka", "Liseberg", "Skansen Kronan", "Masthuggskyrkan", "Nordstan",
    "Chalmers", "Haga", "Röda Sten", "Älvsborgsbron", "Kvarteret Krukan",
    "Göteborgsoperan", "Kungsgatan", "Paddan", "Barken Viking", "Mölndal",
    "Hisingen", "Kviberg", "Majorna", "Västra Frölunda", "Örgryte",
    "Gamlestaden", "Backaplan", "Saltholmen", "Kungsport", "Slottsberget",
    "Masthugget", "Eriksberg", "Skatås", "Delsjön", "Svenska Mässan",
    "Ullevi", "Nya Ullevi", "Lilla Bommen", "Stora Teatern", "Götaplatsen",
    "Göteborgs Konstmuseum", "Stenpiren", "Kålltorp", "Sannegården", "Bagaregården",
    "Redbergslid", "Olskroken", "Brunnsparken", "Möllevången", "Vasa",
    "Gamla Ullevi", "Pölsehallen", "Göteborgs Stadsmuseum", "Heden",
    "Skandia Teatern", "Vinga", "Kortedala", "Tuve", "Länsmansgården",
    "Röda Sten Konsthall", "Gunnebo Slott", "Slottsskogen Djurpark", "Bohus fästning",
    "Sven-Harrys Konstmuseum", "Göteborg Film Festival", "Volvo Torslanda",
    "Lisebergsbanan", "Göteborgs Universitet", "Kronhuset", "Nefertiti",
    "The Göteborg Ghost", "Mölndalsån", "Göta älvbron", "Hjalmar Branting",
    "Kajskjul", "Feskekôrka Smuggler", "Avenyn Sniper", "Linné Spy Point",
    "Bridge Watch", "Hisingen Agents", "Göta Tunnel", "Bergakungen",
    "Mastvind Marknaden", "Skärgårdsön", "Paddan Boats", "Spionkajen",
    "Operahuset", "Göteborgs Spioncentral", "Nordstan Vault", "Backaplan Market",
    "Röda Sten Spy Cell", "Slottsskogen Hideout", "Kungsportsplatsen Rendezvous",
    "Fiskekrogen", "Masthuggsrörelsen", "Haga Codex", "Chalmers Lab",
    "Västra Gatan", "Göteborgs Hemligheter", "Stenpiren Dock", "Gamla Varvet",
    "Älvsborg Fortress", "Kvillebäcken", "Skeppsbron", "Södra Vägen", "Östra Hamngatan",
    "Gamlestads Torg", "Ringön", "Torslanda Airport", "Hisingsbron", "Göteborgs Spionmuseum",
    "Lilla Bommen Spy HQ", "Göteborgs Rännstensgäng", "Feskekôrka Codex",
    "Älvsborgs Fästning", "Röda Sten Smuggling", "Heden Operations", "Vasa Spy Den",
    "Majorna Signal", "Redbergslid Cipher", "Olskroken Surveillance", "Brunnsparken Intel",
    "Göteborg Signalstation", "Nordstan Safehouse", "Kålltorp Hideout",
    "Sannegården Watchtower", "Bagaregården Lookout", "Kviberg Outpost",
    "Skandia Spy Tower", "Vinga Lighthouse", "Tuve Operation Base", "Länsmansgården HQ",
    "Gunnebo Mansion", "Bohus Fortress", "Liseberg Spy Train", "Göteborg Film Spy",
    "Volvo Spy Garage", "The Silent Avenyn", "Göta Tunnel Escape", "Hjalmar Branting Files",
    "Pölsehallen Safezone", "Kajskjul Hideout", "Feskekôrka Fisherman", "Avenyn Night Watch",
    "Linné Spy Nest", "Bridge Surveillance", "Hisingen Spy Network", "Mölndalsån Escape Route",
    "Gamlestaden Spy Ring", "Backaplan Intelligence", "Slottsskogen Espionage",
    "Chalmers Spy Tech", "Göteborg Agent Zero", "Ullevi Secret Meeting",
    "Nya Ullevi Operation", "Stora Teatern Deception", "Götaplatsen Rendezvous",
    "Kronhuset Archive", "Nordic Spy Alliance", "Göteborg Blackout",
    "Masthugget Surveillance", "Eriksberg Spy Dock", "Delsjön Safe Passage",
    "Svenska Mässan Front", "Heden Spy Circle", "Skandia Intelligence Unit",
    "Redbergslid Signal", "Olskroken Cipher", "Brunnsparken Surveillance",
    "Möllevången Spy Market", "Vasa Secret Base", "Gamla Ullevi Intel",
    "Pölsehallen Watchpoint", "Lilla Bommen Spy Dock", "Kortedala Safehouse",
    "Tuve Spy Post", "Länsmansgården Operation", "Röda Sten Smuggling Ring",
    "Kvillebäcken Spy Network", "Skeppsbron Intelligence", "Södra Vägen Lookout",
    "Östra Hamngatan Spy HQ", "Ringön Secret Dock", "Hisingsbron Spy Crossing",
    "Göteborgs Spy Headquarters", "Fiskekrogen Spy Den", "Slottsskogen Spy Outpost",
    "Göteborgs Ghost Agent", "Volvo Spy Unit", "Göteborgs Spionmästare", "Masthugget Spy Den",
    "Paddan Spy Route", "Haga Spy Tunnel", "Liseberg Espionage Team", "Nordstan Spy Shop",
    "Backaplan Spy Warehouse", "Feskekôrka Secret Passage", "Avenyn Spy Watch",
    "Göta älv Spy Bridge", "Skansen Kronan Lookout", "Masthuggskyrkan Signal",
    "Ullevi Spy Dome", "Kungsportsplatsen Spy Station", "Chalmers Spy Lab",
    "Röda Sten Spy Cellar", "Barken Viking Spy Ship", "Göteborgs Spy Fleet",
    "Kvarteret Krukan Spy Hideout", "Göteborgs Spioncentral", "Nordstan Spy Vault",
    "Hisingen Spy Base", "Gamla Varvet Spy Dock", "Älvsborgsbron Spy Passage",
    "Sannegården Spy Den", "Bagaregården Spy Safehouse", "Skatås Spy Tower",
    "Delsjön Spy Retreat", "Svenska Mässan Spy Front", "Lilla Bommen Spy Port",
    "Göteborg Spy Ring", "Backaplan Spy Market", "Göteborg Spy Network"
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

