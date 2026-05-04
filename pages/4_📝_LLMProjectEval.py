import streamlit as st

from widgets.fetch_notifications import fetch_notifications
from widgets.gitlab_config import gitlab_config
from widgets.page_preamble import page_preamble

page_preamble()
fetch_notifications()

st.title("LLM Project Eval")
st.caption("🚧 Work in progress")
st.sidebar.header("LLMProjectEval")
st.write("Evaluate student projects using LLMs and generate structured assessments.")

with st.expander("GitLab Configuration", expanded=True):
    gitlab_config()

gitlab_token = st.session_state.get("gitlab_token")
gitlab_base_url = st.session_state.get("gitlab_base_url")
