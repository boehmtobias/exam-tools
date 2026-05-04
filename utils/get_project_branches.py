import requests
import streamlit as st


@st.cache_data(show_spinner=False)
def get_project_branches(base_url: str, token: str, project_id: int) -> list:
    """Fetch all branches for a project."""
    headers = {"PRIVATE-TOKEN": token}
    branches = []
    page = 1

    while True:
        response = requests.get(
            f"{base_url}/projects/{project_id}/repository/branches",
            headers=headers,
            params={"per_page": 100, "page": page}
        )
        if response.status_code != 200:
            st.error(f"Failed to fetch repository branches: {response.text}")
            break

        batch = response.json()
        if not batch:
            break

        branches.extend(batch)
        page += 1

    return branches
