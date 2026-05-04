import streamlit as st

from utils.get_gitlab_user import get_gitlab_user


def gitlab_config() -> bool:
    auth_is_valid = False

    if "gitlab_base_url" not in st.session_state:
        st.session_state.gitlab_base_url = "https://gitlab.rlp.net/api/v4"
    if "gitlab_token" not in st.session_state:
        st.session_state.gitlab_token = ""

    def handle_change():
        st.session_state["gitlab_base_url"] = st.session_state["_gitlab_base_url_input"]
        st.session_state["gitlab_token"] = st.session_state["_gitlab_token_input"]

    col1, col2 = st.columns([0.6, 0.4])

    with col2:
        st.text_input("GitLab API base URL",
                      value=st.session_state.gitlab_base_url,
                      key="_gitlab_base_url_input",
                      on_change=handle_change,
                      )

    with col1:
        st.text_input("GitLab API personal access token",
                      value=st.session_state.gitlab_token,
                      key="_gitlab_token_input",
                      type="password",
                      on_change=handle_change,
                      help="Requires personal access token with API scope."
                      )

    col3, _ = st.columns([0.6, 0.4])

    with col3:
        uploaded_file = st.file_uploader(
            "Upload .env file with GitLab API token (optional)",
            type=["env"],
            max_upload_size=1,
            accept_multiple_files=False,
            help="Accepted keys: [GITLAB_TOKEN, GITLAB_PERSONAL_ACCESS_TOKEN, GITLAB_API_TOKEN]"
        )

    if uploaded_file is not None:
        content = uploaded_file.getvalue().decode("utf-8")
        token_found = None

        keys_to_search = ["GITLAB_TOKEN", "GITLAB_PERSONAL_ACCESS_TOKEN", "GITLAB_API_TOKEN"]
        for line in content.splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                if key.strip() in keys_to_search:
                    token_found = value.strip().strip('"').strip("'")
                    break

        if token_found:
            if st.session_state.gitlab_token != token_found:
                st.session_state.gitlab_token = token_found
                st.rerun()
        else:
            st.warning("No valid token found.")

    # Authentication logic runs on every page load or interaction
    if st.session_state.gitlab_base_url and st.session_state.gitlab_token:
        request_result = get_gitlab_user(st.session_state.gitlab_base_url, st.session_state.gitlab_token)

        if request_result and request_result["status"] == "success":
            st.success(f"Authenticated as user:&nbsp; **`{request_result['username']}`**")
            auth_is_valid = True
        elif request_result:
            st.error(request_result["message"])

    return auth_is_valid
