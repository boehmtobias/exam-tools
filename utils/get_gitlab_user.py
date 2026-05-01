import streamlit as st
import requests


@st.cache_data(show_spinner="Authenticating with GitLab...")
def get_gitlab_user(url: str, token: str):
    """Checks API access using base URL and token and returns the username or None."""
    if not url or not token:
        return None

    # Use the /user endpoint to verify the token and URL
    api_url = f"{url.rstrip('/')}/user"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(api_url, headers=headers, timeout=5)
        if response.status_code == 200:
            return {"status": "success", "username": response.json().get("username")}
        elif response.status_code == 401:
            return {"status": "error", "message": "Invalid Personal Access Token."}
        elif response.status_code == 404:
            return {"status": "error", "message": "API endpoint not found. Invalid base URL."}
        else:
            return {"status": "error", "message": f"GitLab error (Status {response.status_code})"}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Network error: {e}"}
