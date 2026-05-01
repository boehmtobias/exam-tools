import streamlit as st
from utils.gitlab_config import gitlab_config
st.set_page_config(page_title="LLMIssueFeedback", page_icon="💬")

st.title("LLM Issue Feedback")
st.sidebar.header("LLMIssueFeedback")
st.write("Generate feedback on student GitLab issues using LLMs.")

with st.expander("GitLab Configuration", expanded=True):
    gitlab_config()

gitlab_token = st.session_state.get("gitlab_token")
gitlab_base_url = st.session_state.get("gitlab_base_url")
