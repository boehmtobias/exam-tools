from typing import Any, Dict
import streamlit as st

from utils.get_gitlab_namespaces import get_gitlab_namespaces
from utils.get_gitlab_project_slug import get_gitlab_project_slug
from utils.gitlab_config import gitlab_config

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

st.page_link("ExamUtils.py", label="Back to Main Menu", icon="🎓")
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
# if lock_ui:
#     st.info(
#         "**Authentication Required:** Please provide valid configuration above to proceed.")

st.write("### Namespace Selection")

ns_selected_name = None

if is_authenticated:
    ns_result = get_gitlab_namespaces(
        st.session_state.gitlab_base_url,
        st.session_state.gitlab_token
    )

    if ns_result and ns_result["status"] == "success":
        namespaces = ns_result["data"]

        if namespaces:
            ns_options = {
                n["name"]: n["id"]
                for n in sorted(namespaces, key=lambda x: x["name"].lower())
            }

            col1, col2 = st.columns([2, 1], vertical_alignment="bottom")

            with col1:
                ns_selected_name = st.selectbox(
                    "Select target namespace/group",
                    index=None,
                    options=list(ns_options.keys()),
                    help="Showing groups where you are allowed to create projects (needs at least Developer access)."
                )

            with col2:
                if st.button("Refresh"):
                    get_gitlab_namespaces.clear()
                    st.session_state["_namespaces_refreshed"] = True
                    st.rerun()

            if ns_selected_name:
                ns_selected_id = ns_options[ns_selected_name]

                base_web_url = st.session_state.gitlab_base_url.replace("/api/v4", "").rstrip('/')
                ns_selected_hyperlink = f"{base_web_url}/{ns_selected_name}"

                target_ns_table = f"""
                | Target group name | Target group ID | Open in GitLab |
                | :--- | :--- | :--- |
                | `{ns_selected_name}` | `{ns_selected_id}` | [{ns_selected_hyperlink}]({ns_selected_hyperlink}) |
                """

                st.markdown(target_ns_table)

        else:
            st.warning("No namespaces with project creation permission found (needs at least Developer access).")


    elif ns_result and ns_result["status"] == "error":
        st.error(f"Failed to load namespaces: {ns_result['message']}")

else:
    col1, col2 = st.columns([2, 1], vertical_alignment="bottom")

    with col1:
        st.selectbox("Target namespace/group",
                     index=None,
                     options=[],
                     help="Showing groups where you are allowed to create projects (needs at least Developer access).",
                     disabled=True)
        with col2:
            st.button("Refresh", disabled=True)

st.write("### Project Creation")

init_empty = st.checkbox("Initialize empty repository (without README)",
                         value=True,
                         disabled=(ns_selected_name is None))

project_raw_data = st.text_area("Input project names and slugs",
                                placeholder="First Project, first-project\nSecondProject, custom-slug\nThirdProject",
                                help="Entry format: project name, project slug (optional, generated from name if omitted).",
                                height=250,
                                disabled=(ns_selected_name is None))

parsed_projects = []

if project_raw_data:
    lines = [line.strip() for line in project_raw_data.split('\n') if line.strip()]

    for line in lines:
        parts = line.split(',', 1)

        project_name = parts[0].strip()

        if len(parts) > 1 and parts[1].strip():
            # Slug provided, ensure compatibility with GitLab slugs
            project_slug = get_gitlab_project_slug(parts[1].strip())
        else:
            # No slug provided, so generate from name
            project_slug = get_gitlab_project_slug(project_name)

        parsed_projects.append({"name": project_name, "slug": project_slug})

    if parsed_projects:
        st.markdown(f"**`{len(parsed_projects)}`** projects detected.")

        all_slugs = [p["slug"] for p in parsed_projects]
        has_duplicates = len(all_slugs) != len(set(all_slugs))

        has_empty = any(not p["slug"] for p in parsed_projects)

        if has_duplicates:
            st.error(
                "Duplicate slugs detected: Multiple entries result in the same URL path. GitLab requires unique slugs.")

        if has_empty:
            st.warning("⚠️ Empty Slugs:** One or more projects resulted in an empty slug. Please check your naming.")

        if not has_duplicates and not has_empty:
            pass
