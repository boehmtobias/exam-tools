import streamlit as st

from utils.get_gitlab_user import get_gitlab_user


def gitlab_config():
    if "gitlab_base_url" not in st.session_state:
        st.session_state.gitlab_base_url = "https://gitlab.rlp.net/api/v4"
    if "gitlab_token" not in st.session_state:
        st.session_state.gitlab_token = ""

    def handle_change():
        st.session_state["gitlab_base_url"] = st.session_state["_gitlab_base_url_input"]
        st.session_state["gitlab_token"] = st.session_state["_gitlab_token_input"]

    st.text_input("GitLab API base URL",
                  value=st.session_state.gitlab_base_url,
                  key="_gitlab_base_url_input",
                  on_change=handle_change,
                  )
    st.text_input("GitLab API personal access token",
                  value=st.session_state.gitlab_token,
                  key="_gitlab_token_input",
                  type="password",
                  on_change=handle_change,
                  help="Requires personal access token with API scope."
                  )

    # Authentication logic runs on every page load or interaction
    if st.session_state.gitlab_base_url and st.session_state.gitlab_token:
        request_result = get_gitlab_user(st.session_state.gitlab_base_url, st.session_state.gitlab_token)

        if request_result:
            if request_result["status"] == "success":
                st.success(f"Authenticated as user:&nbsp; **`{request_result['username']}`**")
            else:
                st.error(request_result["message"])
