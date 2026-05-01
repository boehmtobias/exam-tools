import streamlit as st
from utils.gitlab_config import gitlab_config

st.set_page_config(page_title="LLMProjectEval", page_icon="📝")

st.title("LLM Project Eval")
st.sidebar.header("LLMProjectEval")
st.write("Evaluate student projects using LLMs and generate structured assessments.")

with st.expander("GitLab Configuration", expanded=True):
    gitlab_config()

gitlab_token = st.session_state.get("gitlab_token")
gitlab_base_url = st.session_state.get("gitlab_base_url")
