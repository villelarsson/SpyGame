# Spy Game

A small Streamlit app for playing the spy/impostor party game on one shared phone or laptop.

## What it does

1. Enter the number of players (at least 3) and their names.
2. The app picks a random word from a built-in list and makes one random player the spy.
3. The device is passed around. Players see their roles one at a time, in random order: everyone gets the word, except the spy, who is just told they're the spy.
4. After everyone has seen their role, you play the rest of the game out loud (asking questions, voting, and so on). The app doesn't handle that part.
5. "Restart Game" goes back to setup with the names still filled in, so you can start a new round with a new word.

The word list is about 300 everyday Swedish nouns (furniture, kitchen things, clothes, tech and so on). It's hardcoded in `stremlit_spygame.py`. The interface itself is in English.

## Why I built it

I play this game with friends and family and wanted control over the words. Apps for this game decide the word list for you. Here the list is a Python list I can edit whenever I want.

## How to run it

You need Python 3 and Streamlit:

```
pip install streamlit
streamlit run stremlit_spygame.py
```

Streamlit then opens the app in your browser. To change the words, edit the `word_list` in `stremlit_spygame.py`.

## What I'd change

- Move the word list into a separate file (text or JSON), so changing words doesn't mean editing code, and maybe allow several themed lists.
- Remove duplicates from the list. "låda", "ryggsäck", "lock", "bälte" and "keps" each appear more than once, so they get picked more often. A few entries aren't really objects ("golv") or are in plural form ("slevar").
- Fix the "Reveal Role" button. It sets the state but doesn't rerun the app, so the role only shows after a second tap.
- Add an option for more than one spy in bigger groups.
- Have the app pick who asks the first question.
- Add a `requirements.txt` and fix the typo in the filename (`stremlit`). Also remove the unused `base64` import.
