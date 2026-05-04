import streamlit as st

from utils.get_gitlab_namespaces import get_gitlab_namespaces


def namespace_selection(is_auth: bool, key: int = 0, exclude: list = None) -> dict:
    ns_selected_name = None
    ns_selected_id = None
    ns_selected_hyperlink = None
    if exclude is None:
        exclude = []

    if is_auth:
        ns_result = get_gitlab_namespaces(
            st.session_state.gitlab_base_url,
            st.session_state.gitlab_token
        )

        if ns_result and ns_result["status"] == "success":
            namespaces = ns_result["data"]

            if namespaces:
                ns_options = {
                    n["name"]: n["id"]
                    for n in sorted(namespaces, key=lambda x: x["name"].lower())
                    if n["name"] not in exclude
                }

                col1, col2 = st.columns([2, 1], vertical_alignment="bottom")

                with col1:
                    ns_selected_name = st.selectbox(
                        "Select target namespace/group",
                        index=None,
                        options=list(ns_options.keys()),
                        help="Showing groups where you are allowed to create projects (needs at least Developer access).",
                        key=f"ns_selectbox_{key}"
                    )

                with col2:
                    if st.button("Refresh List", key=f"ns_refresh_{key}"):
                        get_gitlab_namespaces.clear()
                        st.session_state["_namespaces_refreshed"] = True
                        st.rerun()

                if ns_selected_name:
                    ns_selected_id = ns_options[ns_selected_name]

                    base_web_url = st.session_state.gitlab_base_url.replace("/api/v4", "").rstrip('/')
                    ns_selected_hyperlink = f"{base_web_url}/{ns_selected_name}"

                    target_ns_table = f"""
                    | Target group name | Target group ID | Open in GitLab |
                    | :--- | :--- | :--- |
                    | `{ns_selected_name}` | `{ns_selected_id}` | [{ns_selected_hyperlink}]({ns_selected_hyperlink}) |
                    """

                    st.markdown(target_ns_table)

            else:
                st.warning("No namespaces with project creation permission found (needs at least Developer access).")


        elif ns_result and ns_result["status"] == "error":
            st.error(f"Failed to load namespaces: {ns_result['message']}")

    else:
        col1, col2 = st.columns([2, 1], vertical_alignment="bottom")

        with col1:
            st.selectbox("Target namespace/group",
                         index=None,
                         options=[],
                         help="Showing groups where you are allowed to create projects (needs at least Developer access).",
                         disabled=True,
                         key=f"ns_selectbox_{key}")

        with col2:
            st.button("Refresh List",
                      disabled=True,
                      key=f"ns_refresh_{key}")

    ns_selection = {"name": ns_selected_name, "id": ns_selected_id, "hyperlink": ns_selected_hyperlink}

    return ns_selection
