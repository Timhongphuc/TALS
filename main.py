import streamlit as st
import os
import psycopg
from dotenv import load_dotenv
import uuid

# Load environment variables from .env file
load_dotenv()

starter = ("The", "A")
adj = (
    "adorable", "clueless", "dirty", "odd", "stupid", "brave", "cheerful",
    "tiny", "gigantic", "sparkly", "mysterious", "ancient", "clever",
    "sleepy", "hungry", "colorful", "noisy", "shy", "friendly", "fierce",
    "polite", "silly", "grumpy", "magical", "curious", "attentive"
)
nouns = (
    "puppy", "car", "rabbit", "girl", "monkey", "cat", "dog", "wizard",
    "pirate", "robot", "teacher", "artist", "dragon", "squirrel", "bicycle",
    "castle", "banana", "astronaut", "penguin", "detective", "guitar",
    "flower", "volcano", "sandwich", "computer", "boy"
)
verbs = (
    "runs", "hits", "jumps", "drives", "barfs", "skips", "sings", "dances",
    "whispers", "laughs", "crawls", "swims", "flies", "builds", "discovers",
    "chases", "cooks", "paints", "reads", "explores", "climbs", "dreams",
    "juggles", "sneezes", "zooms", "writes"
)
adv = (
    "crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally.",
    "bravely.", "quietly.", "quickly.", "slowly.", "happily.", "sadly.",
    "carefully.", "carelessly.", "suddenly.", "boldly.", "gracefully.",
    "loudly.", "secretly.", "eagerly.", "awkwardly.", "politely.",
    "wildly.", "patiently.", "luckily.", "mysteriously.", "badly."
)
# 25^4 combinations of sentences are possible = 390.625 possible sentences (for now in v1)


st.markdown("# [Tim's](https://www.timhongphuc.de/) amazing link shortener 1.0")

link = st.text_input("Enter the link that needs to be shortened", type="url", placeholder="Link")


if link:
    # Get the connection string from the environment variable
    conn_string = os.getenv("DATABASE_URL")

    with psycopg.connect(conn_string) as conn:
        try:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM main-link-storage WHERE link = '{link}'")
                check1 = cur.fetchone()
                if check1 == link:
                    cur.execute(f"SELECT uniqueSentence FROM main-link-storage WHERE link = '{link}'")
        except:

            sentence = "Hello1" #Test

            try:
                with psycopg.connect(conn_string) as conn:
                    print("Connection established")

                    with conn.cursor() as cur:
                        # Insert a link
                        cur.execute(f"""INSERT INTO "main-link-storage" (hyperlink, "uniqueSentence", uuid) VALUES ('{link}', '{sentence}', '{uuid.uuid4()}')""")
                        print("Added a link to library")

            except Exception as e:
                print("Connection failed.")
                print(e)
