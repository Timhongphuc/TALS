import streamlit as st

info_page = st.Page("pages/info.py", title="Information")
add_page = st.Page("pages/add.py", title="Add links")
search_page = st.Page("pages/search.py", title="Search")
#settings_page = st.Page("pages/settings.py", title="Settings")

pg = st.navigation([info_page,search_page,add_page])  # add other logged-in pages here

pg.run()