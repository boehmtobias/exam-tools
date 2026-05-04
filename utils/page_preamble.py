import streamlit as st

def page_preamble() -> None:
    st.set_page_config(
        page_title="ExamTools",
        page_icon="🎓",
        initial_sidebar_state="collapsed")
    st.markdown(
        """
        <style>
        textarea {
            font-family: 'Source Code Pro', 'Monaco', 'Cascadia Code', 'Ubuntu Mono', monospace !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, vertical_alignment="center", width=350, gap="xxsmall")
    with col1:
        st.page_link("ExamUtils.py", label="Back to Main Menu", icon="🎓")
    with col2:
        if st.button("🗑️ Clear All & Start Over", type="tertiary"):
            st.session_state.clear()
            st.cache_data.clear()
            st.rerun()

    return None