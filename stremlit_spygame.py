import streamlit as st
import random

st.set_page_config(page_title="Spy Game", layout="centered")
st.title("🕵️ Spy Game")

# Hårdkodad ordlista (Göteborgs ord)
word_list = [
    # Platser och områden
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
    "Göteborgs Universitet", "Kronhuset", "Nefertiti", "Mölndalsån",
    "Göta älvbron", "Kajskjul", "Göteborgs Konsthall", "Göteborgs Stadsteater",
    "Göteborgs Naturhistoriska Museum", "Göteborgs Botaniska Trädgård",
    "Östra Hamngatan", "Södra Vägen", "Götaleden", "Järntorget",
    "Skärgården", "Delsjöområdet", "Slottsberget", "Kvarnberget",
    "Ruddalen", "Långedrag", "Västra Götaland", "Bohuslän", "Styrsö",
    "Donsö", "Vrångö", "Brännö", "Kungälv", "Torslanda", "Säve", "Majvallen",
    "Öckerö", "Hönö", "Vinga fyr", "Skagen", "Göteborgs Centralstation",
    "Nordstan", "Bohus fästning", "Göteborgs Hamn", "Nya Varvet",
    "Älvsborgs fästning", "Göteborgs Rådhus", "Chalmers Tekniska Högskola",
    "Göteborgs stadsbibliotek", "Göteborgs Konserthus", "Karl Johans Torg",
    "Skatås motionscentrum", "Röda Sten Kulturfabrik", "Kviberg",
    "Vasaplatsen", "Östra sjukhuset", "Linnéstaden", "Guldheden",
    "Haga Nygata", "Kvarteret Krukan", "Göteborgsvarvet", "Volvo Museum",
    "Styrsö Skärgårdsgård", "Långedrags Värdshus", "Sjömagasinet",
    "Göteborgs Konstmuseum", "Haga Kyrka", "Masthuggsbadet", "Saltholmen Färjeläge",
    "Göteborgs Konserthus", "Backaplan Shoppingcenter", "Göteborgs Stadsmissions Second Hand",
    "Trädgårdsföreningen", "Färjenäsparken", "Skärgårdsbåtarna", "Gamlestadstorget",
    "Nordstan Shoppingcenter", "Majvallen Idrottsplats", "Ullevi Stadion",
    "Gamla Ullevi Stadion", "Slottsskogen Djurpark",

    # Kända personer
    "Leif Loket Olsson", "Håkan Hellström", "Zlatan Ibrahimović",
    "Lotta Schelin", "Ingemar Johansson", "Jan Johansson",
    "Bengt Ekerot", "Gösta Ekman", "Peter Forsberg", "Annika Sörenstam",
    "Gunnar Gren", "Henrik Lundqvist", "Lars Winnerbäck", "Greta Garbo",
    "Torgny Segerstedt", "Alfred Nobel", "Anders Celsius", "Jan Troell",
    "Lena Endre", "Björn Ranelid", "Mikael Persbrandt", "Josefin Nilsson",
    "Evert Taube", "Sten Sture", "Maj Sjöwall", "Per Gessle",
    "Camilla Läckberg", "Lasse Kronér", "Björn Borg", "Claes Malmberg",
    "Magnus Uggla", "Lena Philipsson", "Olof Lundh",

    # Fler platser och områden
    "Södra Älvstranden", "Hisingsparken", "Krokslätt", "Brännö Rödsten",
    "Kålltorpsskolan", "Lilla Torget", "Blå Stället", "Olivedal",
    "Skärgårdsbåtsterminalen", "Färjenäs", "Annedal", "Guldhedens sjukhus",
    "Långströmsgatan", "Majornas kyrka", "Vasaplatsens torg", "Östra kyrkogården",
    "Lisebergsstationen", "Kvibergs marknad", "Färjenäsparken", "Hisingsbron",
    "Gamla Teatern", "Lilla Bommen Piren", "Vasagatan", "Hagakyrkan",
    "Kvarnberget lekplats", "Vallgraven", "Bältesspännarparken", "Feskeboa",
    "Kongahälla", "Kvibergs kyrkogård", "Hisingsparken", "Skansen Lejonet",
    "Folkets Park", "Mölndalsån", "Gårda", "Redbergsplatsen", "Majornas torg",
    "Bergsjön", "Lindholmen Science Park", "Biskopsgården",
    "Göteborgs Konstmuseums skulpturpark", "Norra Hamngatan", "Klippan",
    "Säve Flygplats", "Eriksberg kaj", "Käringön", "Skärgårdsmuseet",
    "Torslanda flygplats", "Mellbystrand", "Backaplan", "Sundspromenaden",
    "Askimsbadet", "Kortedala centrum", "Lilla Edet", "Nya Varvet fästning"
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



