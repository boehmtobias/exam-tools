import streamlit as st

from utils.build_namespace_zip import build_namespace_zip
from utils.build_zip_filename import build_zip_filename
from utils.fetch_notifications import fetch_notifications
from utils.format_zip_size import format_zip_size
from utils.gitlab_config import gitlab_config
from utils.namespace_selection import namespace_selection
from utils.page_preamble import page_preamble

page_preamble()
fetch_notifications()

st.title("Export GitLab Projects")
st.sidebar.header("ExportGitLabProjects")
st.write("Download and export GitLab projects from your namespaces and groups.")

with st.expander("GitLab Configuration", expanded=True):
    is_authenticated = gitlab_config()

st.write("### Namespace Selection")

if "ns_count" not in st.session_state:
    st.session_state.ns_count = 1
if "ns_removed" not in st.session_state:
    st.session_state.ns_removed = set()

ns_selections = []
already_selected = []

for i in range(st.session_state.ns_count):
    if i in st.session_state.ns_removed:
        continue
    with st.container(border=True):
        st.write(f"#### Target Namespace {i + 1}")
        ns = namespace_selection(is_auth=is_authenticated, key=i, exclude=already_selected)
        if i != 0 and st.button("❌", key=f"ns_remove_{i}"):
            st.session_state.ns_removed.add(i)
            st.rerun()
    ns_selections.append(ns)
    if ns["name"] and ns["name"] not in already_selected:
        already_selected.append(ns["name"])

if st.button("➕ Add Another", disabled=not is_authenticated):
    st.session_state.ns_count += 1
    st.rerun()

st.write("### Download")
st.write("Exports all branches for all projects/repositories within the selected namespaces.")

active_selections = [ns for ns in ns_selections if ns["id"]]
has_selections = bool(active_selections)

if st.button("⬇️ Pull Projects", disabled=not has_selections):
    st.session_state.prepared_zips = {}

    for ns in active_selections:
        with st.spinner(f"Building zip for **{ns['name']}**..."):
            zip_bytes, project_count = build_namespace_zip(
                st.session_state.gitlab_base_url,
                st.session_state.gitlab_token,
                ns
            )
            filename = build_zip_filename(ns["name"])
            st.session_state.prepared_zips[ns["name"]] = {
                "bytes": zip_bytes,
                "filename": filename,
                "project_count": project_count,
                "size": len(zip_bytes)
            }

if "prepared_zips" in st.session_state and st.session_state.prepared_zips:
    items = list(st.session_state.prepared_zips.items())
    for i in range(0, len(items), 2):
        cols = st.columns(2)
        for j, (ns_name, info) in enumerate(items[i:i + 2]):
            with cols[j]:
                with st.container(border=True):
                    st.write(f"##### **{ns_name}**")
                    st.write(
                        f"📝 Filename: **`{info['filename']}`**  \n"
                        f"📂 Amount: **`{info['project_count']} projects`**  \n"
                        f"💾 Download Size: **`{format_zip_size(info['size'])}`**"
                    )
                    st.download_button(
                        label="📥 Download",
                        type="primary",
                        data=info["bytes"],
                        file_name=info["filename"],
                        mime="application/zip",
                        key=f"dl_{ns_name}"
                    )
