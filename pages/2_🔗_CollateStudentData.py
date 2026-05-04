import streamlit as st

from utils.fetch_notifications import fetch_notifications
from utils.gitlab_config import gitlab_config
from utils.page_preamble import page_preamble

page_preamble()
fetch_notifications()

st.title("Collate Student Data")
st.sidebar.header("CollateStudentData")
st.write("Aggregate and organize student data from multiple sources.")

with st.expander("GitLab Configuration", expanded=True):
    gitlab_config()

gitlab_token = st.session_state.get("gitlab_token")
gitlab_base_url = st.session_state.get("gitlab_base_url")
