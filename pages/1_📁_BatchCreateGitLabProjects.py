import streamlit as st

from ui.fetch_notifications import fetch_notifications
from utils.get_gitlab_project_slug import get_gitlab_project_slug
from ui.gitlab_config import gitlab_config
from ui.namespace_selection import namespace_selection
from ui.page_preamble import page_preamble

page_preamble()
fetch_notifications()

st.title("Batch Create GitLab Projects")
st.caption("🚧 Work in progress")
st.sidebar.header("BatchCreateGitLabProjects")
st.write("Create GitLab projects as needed across your namespaces and groups in one go.")

with st.expander("GitLab Configuration", expanded=True):
    is_authenticated = gitlab_config()

st.write("### Namespace Selection")

ns_selection = namespace_selection(is_auth=is_authenticated)

st.write("### Project Creation")

init_empty = st.checkbox("Initialize empty repository (without README)",
                         value=True,
                         disabled=(ns_selection["name"] is None))

project_raw_data = st.text_area("Input project names and slugs",
                                placeholder="First Project, first-project\nSecondProject, custom-slug\nThirdProject",
                                help="Entry format: project name, project slug (optional, generated from name if omitted).",
                                height=250,
                                disabled=(ns_selection["name"] is None))

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
