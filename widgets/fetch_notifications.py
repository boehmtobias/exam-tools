import streamlit as st

def fetch_notifications() -> None:
    # namespace_selection(): Toast message send upon page reload
    if st.session_state.get("_namespaces_refreshed"):
        st.toast("Namespace list updated!")
        del st.session_state["_namespaces_refreshed"]

    return None