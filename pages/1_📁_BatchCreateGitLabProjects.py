from typing import Any, Dict
import streamlit as st

from utils.get_gitlab_namespaces import get_gitlab_namespaces
from utils.gitlab_config import gitlab_config

st.set_page_config(page_title="BatchCreateGitLabProjects", page_icon="📁")

st.title("Batch Create GitLab Projects")
st.sidebar.header("BatchCreateGitLabProjects")
st.write("Create GitLab projects as needed across your namespaces and groups in one go.")

# Toast message send upon page reload
if st.session_state.get("_namespaces_refreshed"):
    st.toast("Namespace list updated!")
    del st.session_state["_namespaces_refreshed"]

with st.expander("GitLab Configuration", expanded=True):
    is_authenticated = gitlab_config()

lock_ui = not is_authenticated
if lock_ui:
    st.info(
        "**Authentication Required:** Please provide valid configuration above to proceed.")

st.write("### Select Namespace")

if is_authenticated:
    ns_result = get_gitlab_namespaces(
        st.session_state.gitlab_base_url,
        st.session_state.gitlab_token
    )

    if ns_result and ns_result["status"] == "success":
        namespaces = ns_result["data"]

        if namespaces:
            ns_options = {n["name"]: n["id"] for n in namespaces}

            col1, col2 = st.columns([5, 1], vertical_alignment="bottom")

            with col1:
                ns_selected_name = st.selectbox(
                    "Select target namespace/group",
                    index=None,
                    options=list(ns_options.keys()),
                    help="Showing groups where you are allowed to create projects (needs at least Developer access)."
                )

            with col2:
                if st.button("Refresh List"):
                    get_gitlab_namespaces.clear()
                    st.session_state["_namespaces_refreshed"] = True
                    st.rerun()

            if ns_selected_name:
                ns_selected_id = ns_options[ns_selected_name]

                target_ns_table = f"""
                | Target group name | Target group ID |
                | :--- | :--- |
                | `{ns_selected_name}` | `{ns_selected_id}` |
                """

                st.markdown(target_ns_table)

        else:
            st.warning("No namespaces with project creation permission found (needs at least Developer access).")


    elif ns_result and ns_result["status"] == "error":
        st.error(f"Failed to load namespaces: {ns_result['message']}")

else:
    col1, col2 = st.columns([5, 1], vertical_alignment="bottom")

    with col1:
        st.selectbox("Select Target Namespace/Group",
                     index=None,
                     options=[],
                     help="Showing groups where you are allowed to create projects (needs at least Developer access).",
                     disabled=True)
        with col2:
            st.button("Refresh List", disabled=True)
