from typing import Any, Dict
import streamlit as st

from utils.gitlab_config import gitlab_config

st.set_page_config(page_title="BatchCreateGitLabProjects", page_icon="📁")

st.title("Batch Create GitLab Projects")
st.sidebar.header("BatchCreateGitLabProjects")
st.write("Create GitLab projects as needed across your namespaces and groups in one go.")

with st.expander("GitLab Configuration", expanded=True):
    gitlab_config()

gitlab_token = st.session_state.get("gitlab_token")
gitlab_base_url = st.session_state.get("gitlab_base_url")
