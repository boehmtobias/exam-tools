import streamlit as st

from utils.fetch_notifications import fetch_notifications
from utils.gitlab_config import gitlab_config
from utils.namespace_selection import namespace_selection

st.set_page_config(
    page_title="ExamTools",
    page_icon="🎓",
    initial_sidebar_state="collapsed")
st.markdown(
    """
    <style>
    textarea {
        font-family: 'Source Code Pro', 'Monaco', 'Cascadia Code', 'Ubuntu Mono', monospace !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
fetch_notifications()

st.page_link("ExamUtils.py", label="Back to Main Menu", icon="🎓")
st.title("Export GitLab Projects")
st.sidebar.header("ExportGitLabProjects")
st.write("Download and export GitLab projects from your namespaces and groups.")

with st.expander("GitLab Configuration", expanded=True):
    is_authenticated = gitlab_config()

st.write("### Namespace Selection")

ns_selection = namespace_selection(is_auth=is_authenticated)