import io
import zipfile

import requests
import streamlit as st

from utils.get_namespace_repositories import get_namespace_repositories
from utils.get_project_branches import get_project_branches


@st.cache_data(show_spinner=False)
def _download_branch_archive(base_url: str, token: str, project_id: int, branch_name: str) -> bytes | None:
    """Download a single branch as a zip archive, returns raw bytes or None on failure."""
    headers = {"PRIVATE-TOKEN": token}

    response = requests.get(
        f"{base_url}/projects/{project_id}/repository/archive.zip",
        headers=headers,
        params={"sha": branch_name},
        stream=True
    )

    if response.status_code != 200:
        st.error(f"Failed to download branch archive: {response.text}")
        return None

    return response.content


def build_namespace_zip(base_url: str, token: str, ns: dict) -> tuple[bytes, int]:
    """
    Build a zip for one namespace.
    Structure: repo_name/branch_name/<contents>
    Returns (zip_bytes, project_count).
    """
    master_buffer = io.BytesIO()
    project_count = 0

    repos = get_namespace_repositories(base_url, token, ns["id"])
    if not repos:
        st.warning(f"No repositories found in `{ns['name']}`.")
        return master_buffer.getvalue(), 0

    progress = st.progress(0, text=f"Starting download for {ns['name']}...")

    with zipfile.ZipFile(master_buffer, "w", zipfile.ZIP_DEFLATED) as master_zip:
        for i, project in enumerate(repos):
            repo_name = project["path"]
            project_id = project["id"]

            branches = get_project_branches(base_url, token, project_id)

            if not branches:
                progress.progress((i + 1) / len(repos), text=f"Skipping `{repo_name}` (no branches)...")
                continue

            for branch in branches:
                branch_name = branch["name"]
                progress.progress(
                    (i + 1) / len(repos),
                    text=f"`{repo_name}` — branch `{branch_name}`..."
                )

                archive_bytes = _download_branch_archive(base_url, token, project_id, branch_name)

                if not archive_bytes:
                    st.warning(f"Failed to download `{repo_name}/{branch_name}`.")
                    continue

                # The archive from GitLab is a zip, so extract and re-package under repo_name/branch_name/
                with zipfile.ZipFile(io.BytesIO(archive_bytes)) as branch_zip:
                    for entry in branch_zip.namelist():
                        # Strip GitLab top-level folder wrapper
                        parts = entry.split("/", 1)
                        inner_path = parts[1] if len(parts) > 1 else parts[0]
                        if not inner_path:
                            continue

                        target_path = f"{repo_name}/{branch_name}/{inner_path}"
                        master_zip.writestr(target_path, branch_zip.read(entry))

            project_count += 1

    progress.empty()
    master_buffer.seek(0)
    return master_buffer.getvalue(), project_count
