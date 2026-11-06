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

st.markdown("# TALS Search")

sentence = st.text_input("Enter the magic sentence", type="default", placeholder="Magic Sentence")


if sentence:
    # Get the connection string from the environment variable
    conn_string = os.getenv("DATABASE_URL")

    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()

    #st.button("Rerun")

    with psycopg.connect(conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT "uniqueSentence" FROM "main-link-storage" WHERE "uniqueSentence" = %s""", (sentence,)) #?
                check1 = cur.fetchone() # Response is ALWAYS a tuple somehow...
                if check1 is not None:
                    cur.execute("""SELECT hyperlink FROM "main-link-storage" WHERE "uniqueSentence" = %s""", (sentence,)) #? - I URGENTLY NEED TO ATTEND SQL 101
                    found_sentence = cur.fetchone()
                    link_in_db = found_sentence[0]

                    st.markdown("### The link exists and already got indexed")
                    st.markdown("### Your magic link is:")
                    st.markdown(f"### <u>{link_in_db}</u>", unsafe_allow_html=True)
                    print(f"The matching link is: {link_in_db}")


                else:
                    st.markdown("## This magic sentence does not exist")