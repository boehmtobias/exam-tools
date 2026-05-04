import requests
import streamlit as st


@st.cache_data(show_spinner=False)
def get_namespace_repositories(base_url: str, token: str, namespace_id: int) -> list:
    """Fetch all repositories in a namespace."""
    headers = {"PRIVATE-TOKEN": token}
    repos = []
    page = 1

    while True:
        response = requests.get(
            f"{base_url}/groups/{namespace_id}/projects",
            headers=headers,
            params={"per_page": 100, "page": page, "include_subgroups": True}
        )
        if response.status_code != 200:
            st.error(f"Failed to fetch repositories: {response.text}")
            break

        batch = response.json()
        if not batch:
            break

        repos.extend(batch)
        page += 1

    return repos
