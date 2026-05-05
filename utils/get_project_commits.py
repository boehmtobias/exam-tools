import streamlit as st
import requests


@st.cache_data(show_spinner=False)
def get_project_commits(base_url: str, token: str, project_id: int, branch_name: str) -> list[dict]:
    """
    Fetch all commits for a given project branch via the GitLab API.

    Returns a list of dicts with keys:
        - id          (full SHA)
        - short_id    (abbreviated SHA)
        - authored_date
        - author_name
        - message
    """
    headers = {"PRIVATE-TOKEN": token}
    commits: list[dict] = []
    page = 1

    while True:
        response = requests.get(
            f"{base_url}/projects/{project_id}/repository/commits",
            headers=headers,
            params={
                "ref_name": branch_name,
                "per_page": 100,
                "page": page,
            },
        )

        if response.status_code != 200:
            st.warning(
                f"Could not fetch commits for project {project_id} "
                f"branch `{branch_name}`: {response.status_code}"
            )
            break

        batch = response.json()
        if not batch:
            break

        for c in batch:
            commits.append(
                {
                    "id": c.get("id", ""),
                    "short_id": c.get("short_id", ""),
                    "authored_date": c.get("authored_date", ""),
                    "author_name": c.get("author_name", ""),
                    "message": c.get("message", "").strip(),
                }
            )

        if len(batch) < 100:
            break

        page += 1

    return commits