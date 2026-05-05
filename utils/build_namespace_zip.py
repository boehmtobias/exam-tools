import io
import zipfile

import requests
import streamlit as st

from utils.get_namespace_repositories import get_namespace_repositories
from utils.get_project_branches import get_project_branches
from utils.get_project_commits import get_project_commits


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


def _build_url_file(project_web_url: str) -> str:
    """Return the contents of a Windows-compatible .url shortcut file."""
    return f"[InternetShortcut]\nURL={project_web_url}\n"

def _build_webloc_file(project_web_url: str) -> str:
    """Return the contents of a macOS-compatible .webloc shortcut file."""
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"'
        ' "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
        '<plist version="1.0">\n'
        '<dict>\n'
        '    <key>URL</key>\n'
        f'    <string>{project_web_url}</string>\n'
        '</dict>\n'
        '</plist>\n'
    )


def _build_commits_markdown(
        project_name: str,
        project_web_url: str,
        commits_by_branch: dict[str, list[dict]],
) -> str:
    """
    Render commits from all branches as a .md document.

    Columns: #  |  Branch  |  SHA  |  Date  |  Author  |  Message
    """
    total = sum(len(c) for c in commits_by_branch.values())

    lines: list[str] = [
        f"# Commit History — {project_name}",
        "",
        f"Repository: {project_web_url}  ",
        f"Total commits: {total}",
        "",
        "| # | Branch | SHA | Date | Author | Message |",
        "|---|--------|-----|------|--------|---------|",
    ]

    idx = 1
    all_commits: list[dict] = []

    for branch_name, commits in commits_by_branch.items():
        for c in commits:
            author = c["author_name"].replace("|", "\\|")
            first_line = c["message"].splitlines()[0].replace("|", "\\|") if c["message"] else ""
            date = c["authored_date"][:10]
            sha_link = f"[`{c['short_id']}`]({project_web_url}/-/commit/{c['id']})"

            lines.append(f"| {idx} | `{branch_name}` | {sha_link} | {date} | {author} | {first_line} |")
            idx += 1
            all_commits.append(c)

    # Full messages for multi-line commits
    multi = [c for c in all_commits if len(c["message"].splitlines()) > 1]
    if multi:
        lines += ["", "---", "", "## Full Commit Messages", ""]
        for c in multi:
            lines += [
                f"### `{c['short_id']}` — {c['authored_date'][:10]} — {c['author_name']}",
                "",
                "```",
                c["message"],
                "```",
                "",
            ]

    return "\n".join(lines)


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
            project_web_url = project.get("web_url", "")
            project_count += 1

            branches = get_project_branches(base_url, token, project_id)

            if not branches:
                progress.progress((i + 1) / len(repos), text=f"Skipping `{repo_name}` (no branches)...")
                master_zip.writestr(f"{repo_name}/.empty", "")
                continue

            # Write web link shortcuts
            if project_web_url:
                master_zip.writestr(
                    f"{repo_name}/{repo_name}.url",
                    _build_url_file(project_web_url),
                )
                master_zip.writestr(
                    f"{repo_name}/{repo_name}.webloc",
                    _build_webloc_file(project_web_url),
                )

            commits_by_branch = {}
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

                commits_by_branch[branch_name] = get_project_commits(
                    base_url, token, project_id, branch_name
                )

            if commits_by_branch:
                commits_md = _build_commits_markdown(
                    project_name=repo_name,
                    project_web_url=project_web_url,
                    commits_by_branch=commits_by_branch,
                )
                master_zip.writestr(f"{repo_name}/COMMITS.md", commits_md)

    progress.empty()
    master_buffer.seek(0)
    return master_buffer.getvalue(), project_count
