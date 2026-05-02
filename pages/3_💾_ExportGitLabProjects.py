import streamlit as st
from utils.gitlab_config import gitlab_config

st.set_page_config(
    page_title="ExamTools",
    page_icon="🎓",
    initial_sidebar_state="collapsed")

st.title("Export GitLab Projects")
st.sidebar.header("ExportGitLabProjects")
st.write("Download and export GitLab projects from your namespaces and groups.")

with st.expander("GitLab Configuration", expanded=True):
    gitlab_config()

gitlab_token = st.session_state.get("gitlab_token")
gitlab_base_url = st.session_state.get("gitlab_base_url")
