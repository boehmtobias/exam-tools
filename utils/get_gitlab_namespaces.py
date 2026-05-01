import streamlit as st
import requests


@st.cache_data(ttl=3600, show_spinner="Fetching accessible namespaces...")
def get_gitlab_namespaces(url: str, token: str):
    if not url or not token:
        return None

    api_url = f"{url.rstrip('/')}/groups"
    # min_access_level 30 = Developer, 40 = Maintainer
    params = {"min_access_level": 30, "per_page": 100}
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(api_url, headers=headers, params=params, timeout=15)

        if response.status_code == 200:
            try:
                data = response.json()
                namespaces = [{"name": g["full_path"], "id": g["id"]} for g in data]
                return {"status": "success", "data": namespaces}
            except ValueError:
                return {"status": "error", "message": "Value error: Server failed to return JSON."}

        elif response.status_code == 401:
            return {"status": "error", "message": "Unauthorized: Invalid Token."}
        elif response.status_code == 403:
            return {"status": "error", "message": "Forbidden: You don't have permission to list groups."}
        else:
            return {"status": "error", "message": f"GitLab error (Status {response.status_code})"}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Network error: {e}"}