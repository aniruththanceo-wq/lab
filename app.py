import streamlit as st
import runpy

st.set_page_config(page_title="Experiment 1", page_icon="🔍")

st.title("Experiment 1 - Interpolation Search")

if st.button("Run Experiment"):
    runpy.run_path("Experiment 1.py")
