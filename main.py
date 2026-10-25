import streamlit as st
import os
import psycopg
from dotenv import load_dotenv
import uuid
import random
import time
from datetime import datetime

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

    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()

    st.button("Rerun")

    with psycopg.connect(conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT hyperlink FROM "main-link-storage" WHERE hyperlink = %s""", (link,)) #?
                check1 = cur.fetchone() # Response is ALWAYS a tuple somehow...
                if check1 is not None:
                    cur.execute("""SELECT "uniqueSentence" FROM "main-link-storage" WHERE hyperlink = %s""", (link,)) #? - I URGENTLY NEED TO ATTEND SQL 101
                    found_sentence = cur.fetchone()
                    magic_sentence = found_sentence[0]

                    st.markdown("## The link exists and already got indexed")
                    st.markdown("### Your magic sentence is:")
                    st.markdown(f"### <u>{magic_sentence}</u>", unsafe_allow_html=True)
                    print(f"The magic sentence is: {magic_sentence}")


                else:

                    sentence = f"{random.choice(starter)} {random.choice(adj)} {random.choice(nouns)} {random.choice(verbs)} {random.choice(adv)}"

                    try:
                        with psycopg.connect(conn_string) as conn:
                            print("Connection established")

                            with conn.cursor() as cur:
                                # Insert a link
                                cur.execute("""INSERT INTO "main-link-storage" (hyperlink, "uniqueSentence", uuid, date) VALUES (%s, %s, %s, %s)""", (link, sentence, uuid.uuid4(), datetime.now()))
                                print("Added a link to library")

                                recently_added = sentence

                                cur.execute("""SELECT "uniqueSentence"
                                               FROM "main-link-storage"
                                               WHERE "uniqueSentence" = %s""", (recently_added,))  # ? - I URGENTLY NEED TO ATTEND SQL 101 (#2)
                                found_sentence = cur.fetchone()
                                magic_sentence = found_sentence[0]

                                st.markdown("## The link got indexed and added to the public library")
                                st.markdown("### Your magic sentence is:")
                                st.markdown(f"### <u>{sentence}</u>", unsafe_allow_html=True)


                                sentence = ""

                    except Exception as e:
                        print("Connection failed.")
                        print(e)