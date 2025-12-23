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
    # Hårdkodad ordlista – ca 300 vanliga svenska substantiv (föremål/saker)
    st.session_state.word_list = [
        # Transport & rörelse
        "bil", "cykel", "buss", "tåg", "spårvagn", "båt", "färja", "motorcykel",
        "sparkcykel", "lastbil", "släp", "hjul", "däck", "ratt", "bälte",

        # Möbler
        "bord", "stol", "soffa", "säng", "fåtölj", "pall", "bänk", "hylla",
        "garderob", "byrå", "sängbord", "bokhylla", "skåp", "låda", "spegel",

        # Belysning & el
        "lampa", "taklampa", "golvlampa", "fönsterlampa", "glödlampa",
        "strömbrytare", "eluttag", "sladd", "kabel", "förlängningssladd",

        # Teknik
        "telefon", "mobil", "dator", "laptop", "surfplatta", "skärm",
        "tangentbord", "mus", "hörlurar", "högtalare", "mikrofon",
        "kamera", "webbkamera", "router", "modem", "usb-minne",
        "hårddisk", "laddare", "batteri", "powerbank",

        # Kök – porslin & bestick
        "tallrik", "assiett", "skål", "fat", "glas", "vinglas", "mugg", "kopp",
        "kniv", "gaffel", "sked", "tesked", "slevar", "visp", "tång",

        # Kök – redskap
        "stekpanna", "kastrull", "lock", "skärbräda", "rivjärn", "sil",
        "durkslag", "osthyvel", "potatisskalare", "korkskruv",
        "konservöppnare", "brödrost", "vattenkokare", "kaffebryggare",
        "espressomaskin", "mikrovågsugn", "ugn", "spis",

        # Vitvaror
        "kylskåp", "frys", "diskmaskin", "tvättmaskin", "torktumlare",
        "dammsugare", "fläkt", "element", "avfuktare",

        # Städ & hushåll
        "mopp", "hink", "svabb", "trasa", "svamp", "diskmedel",
        "tvättmedel", "sköljmedel", "soppåse", "soptunna", "sopskyffel",
        "borste", "diskborste", "handdisk", "golv",

        # Badrum & hygien
        "handduk", "badhandduk", "tvål", "schampo", "balsam", "duschgel",
        "tandborste", "tandkräm", "tandtråd", "rakapparat", "rakhyvel",
        "toapapper", "pappershandduk", "tvättkorg", "badmatta",

        # Kläder & accessoarer
        "jacka", "kappa", "tröja", "t-shirt", "skjorta", "byxor",
        "jeans", "kjol", "klänning", "strumpor", "skor", "stövlar",
        "sneakers", "mössa", "keps", "hatt", "halsduk", "vantar",
        "handskar", "bälte", "plånbok", "handväska", "ryggsäck",

        # Kontor & skola
        "bok", "anteckningsbok", "tidning", "häfte", "papper",
        "penna", "blyertspenna", "suddgummi", "linjal", "överstrykningspenna",
        "pärm", "mapp", "postit", "kalender", "almanacka",
        "skrivbord", "kontorsstol", "brev", "kuvert", "stämpel",

        # Förvaring & material
        "kartong", "låda", "påse", "plastpåse", "papperspåse",
        "ryggsäck", "väska", "resväska", "necessär",
        "plastburk", "glasburk", "lock",

        # Hem & småsaker
        "nyckel", "nyckelknippa", "fjärrkontroll", "klocka", "väckarklocka",
        "timer", "termometer", "brandvarnare", "låda", "krok",
        "galge", "tvättnypa", "säkerhetsnål", "tejp", "sax",
        "lim", "måttband", "verktyg", "skruvmejsel", "hammare",

        # Ute & fritid
        "cykelhjälm", "ryggsäck", "picknickfilt", "vattenflaska",
        "termos", "grill", "tändare", "ficklampa",
        "paraply", "regnjacka", "solglasögon", "keps",

        # Övrigt vardagligt
        "matta", "gardin", "kudde", "täcke", "lakan",
        "fönster", "dörr", "handtag", "lås", "ringklocka"
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
