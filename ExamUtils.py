import streamlit as st

st.set_page_config(page_title="ExamUtils", page_icon="🎓")

st.title("ExamUtils")
st.sidebar.header("ExamUtils")
st.write("A collection of utilities for portfolio exams.")

col1, col2, col3 = st.columns(3, border=True)

with col1:
    st.markdown("#### 📁 Batch Create GitLab Projects")
    st.write("Create GitLab projects across your namespaces and groups in one go.")
    st.page_link("pages/1_📁_BatchCreateGitLabProjects.py", label="Open →")

with col2:
    st.markdown("#### 🔗 Collate Student Data")
    st.write("Aggregate and organize student data from multiple sources.")
    st.page_link("pages/2_🔗_CollateStudentData.py", label="Open →")

with col3:
    st.markdown("#### 💾 Export GitLab Projects")
    st.write("Download and export GitLab projects from your namespaces and groups.")
    st.page_link("pages/3_💾_ExportGitLabProjects.py", label="Open →")


col4, col5, _ = st.columns(3)

with col4:
    with st.container(border=True):
        st.markdown("#### 📝 LLM Project Eval")
        st.write("Evaluate student projects using LLMs and generate structured assessments.")
        st.page_link("pages/4_📝_LLMProjectEval.py", label="Open →")

with col5:
    with st.container(border=True):
        st.markdown("#### 💬 LLM Issue Feedback")
        st.write("Generate feedback on student GitLab issues using LLMs.")
        st.page_link("pages/5_💬_LLMIssueFeedback.py", label="Open →")
