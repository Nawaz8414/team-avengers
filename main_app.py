import streamlit as st
from PyPDF2 import PdfReader
from ai_engine import analyze_jobseeker
from chat_ai import generate_chat_response
import pandas as pd


def run_main_app():

    st.markdown("""
    <h1 style='text-align:center;'>🤖 Intelligent Jobseeker Engagement Platform</h1>
    <hr>
    """, unsafe_allow_html=True)

    # ================= LOGOUT =================
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()

    # ================= SESSION STATE =================
    st.session_state.setdefault("single_result", None)
    st.session_state.setdefault("multi_results", {})
    st.session_state.setdefault("chat_jobseeker", [])
    st.session_state.setdefault("chat_recruiter", [])
    st.session_state.setdefault("chat_loading", False)

    # ================= MODE =================
    platform_mode = st.radio(
        "Select Platform Mode",
        ["Single Resume (Jobseeker)", "Multi Resume (Recruiter)"],
        horizontal=True
    )

    left, main, right = st.columns([1.3, 3, 1.5])

    # ================= JOB DATABASE =================
    job_database = [
        {"job_title": "Frontend Developer", "required_skills": ["HTML", "CSS", "JavaScript", "React"]},
        {"job_title": "Backend Developer", "required_skills": ["Python", "Node", "SQL"]},
    ]

    # =========================================================
    # ================= SINGLE RESUME =========================
    # =========================================================
    if platform_mode == "Single Resume (Jobseeker)":

        with left:
            st.header("📄 Upload Resume")
            resume_text = ""
            file = st.file_uploader("Upload PDF", type="pdf")

            if file:
                reader = PdfReader(file)
                for p in reader.pages:
                    resume_text += p.extract_text() or ""

            last_active_days = st.number_input("Days Since Last Activity", 0, 365, 10)
            analyze = st.button("Analyze Resume", use_container_width=True)

        if analyze and resume_text.strip():
            st.session_state.single_result = analyze_jobseeker(
                resume_text,
                job_database,
                last_active_days
            )

        with main:
            if st.session_state.single_result:
                res = st.session_state.single_result

                analyzed_role = res["skill_gap_analysis"]["target_role_used"]
                role_score = res["job_recommendations"][0]["match_percentage"]

                st.info(f" Analyzed Role: **{analyzed_role}** | Match: **{role_score}%**")

                c1, c2, c3 = st.columns(3)
                c1.metric("Resume Score", res["resume_analysis"]["resume_strength_score"])
                c2.metric("Skills Found", len(res["resume_analysis"]["top_skills"]))
                c3.metric("Top Match", f"{role_score}%")

                tab1, tab2, tab3 = st.tabs(
                    ["Resume Analysis", "Skill Gap", "Interview Prep"]
                )

                with tab1:
                    st.subheader("Skills")
                    for s in res["resume_analysis"]["top_skills"]:
                        st.write("•", s)

                    st.subheader("Suggestions")
                    for s in res["resume_analysis"]["improvement_suggestions"]:
                        st.write("•", s)

                with tab2:
                    st.subheader("Missing Skills")
                    for s in res["skill_gap_analysis"]["missing_skills"]:
                        st.write("•", s)

                # ✅ RESTORED OLD INTERVIEW PREP
                with tab3:
                    st.subheader("Technical Questions")
                    for q in res["interview_prep"]["technical_questions"]:
                        st.write("•", q)

                    st.subheader("Behavioral Questions")
                    for q in res["interview_prep"]["behavioral_questions"]:
                        st.write("•", q)

            else:
                st.info("Upload and analyze resume.")

        # ================= CHAT =================
        with right:
            st.header("Career Coach")

            chat_box = st.container(height=420)
            with chat_box:
                for r, m in st.session_state.chat_jobseeker:
                    st.markdown(f"**{r}:** {m}")

            msg = st.text_input("Ask about your resume")

            if st.button("Send", disabled=st.session_state.chat_loading):
                if st.session_state.single_result and msg.strip():
                    st.session_state.chat_loading = True
                    with st.spinner("AI is thinking..."):
                        reply = generate_chat_response(
                            msg,
                            st.session_state.single_result,
                            "jobseeker",
                            st.session_state.chat_jobseeker
                        )
                    st.session_state.chat_jobseeker += [("You", msg), ("AI", reply)]
                    st.session_state.chat_loading = False
                    st.rerun()

    # =========================================================
    # ================= MULTI RESUME ==========================
    # =========================================================
    else:

        with left:
            st.header("📂 Upload Multiple Resumes")
            files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
            analyze_all = st.button("Analyze All", use_container_width=True)

        if analyze_all and files:
            st.session_state.multi_results.clear()

            for f in files:
                text = ""
                reader = PdfReader(f)
                for p in reader.pages:
                    text += p.extract_text() or ""

                st.session_state.multi_results[f.name] = analyze_jobseeker(
                    text,
                    job_database,
                    0
                )

        with main:
            if st.session_state.multi_results:
                leaderboard = []
                for name, res in st.session_state.multi_results.items():
                    leaderboard.append({
                        "Candidate": name,
                        "Score": res["resume_analysis"]["resume_strength_score"],
                        "Top Match %": res["job_recommendations"][0]["match_percentage"]
                    })

                df = pd.DataFrame(leaderboard).sort_values(by="Score", ascending=False)
                st.dataframe(df, use_container_width=True)

        with right:
            st.header(" Recruiter Assistant")

            chat_box = st.container(height=420)
            with chat_box:
                for r, m in st.session_state.chat_recruiter:
                    st.markdown(f"**{r}:** {m}")

            msg = st.text_input("Ask about candidates")

            if st.button("Send", disabled=st.session_state.chat_loading):
                if st.session_state.multi_results and msg.strip():
                    st.session_state.chat_loading = True
                    with st.spinner("AI is thinking..."):
                        reply = generate_chat_response(
                            msg,
                            st.session_state.multi_results,
                            "recruiter",
                            st.session_state.chat_recruiter
                        )
                    st.session_state.chat_recruiter += [("You", msg), ("AI", reply)]
                    st.session_state.chat_loading = False
                    st.rerun()