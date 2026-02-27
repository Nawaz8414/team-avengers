import streamlit as st
from main_app import run_main_app
from auth import authenticate_user, create_user

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Intelligent Jobseeker Platform",
    layout="wide"
)

st.markdown("""
<style>
/* ---------- GLOBAL BACKGROUND ---------- */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* ---------- REMOVE STREAMLIT PADDING ---------- */
.block-container {
    padding-top: 2rem;
}

/* ---------- GLASS CARD ---------- */
.glass-card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 22px;
    height: 100%;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    border: 1px solid rgba(255,255,255,0.15);
}

/* ---------- HERO TITLE ---------- */
.hero-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
}

.hero-subtitle {
    text-align: center;
    font-size: 18px;
    color: #d1d5db;
}

/* ---------- TOP RIGHT BUTTONS ---------- */
.auth-btn button {
    width: 100%;
    border-radius: 12px !important;
}


</style>
""", unsafe_allow_html=True)

# ================= SESSION STATE =================
st.session_state.setdefault("page", "landing")   # landing | login | signup | app
st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("user", None)


# ================= LANDING PAGE =================
def landing_page():

    # ---------- TOP RIGHT LOGIN / SIGNUP ----------
    colX, colY, colZ = st.columns([6, 1.2, 1.2])
    with colY:
        if st.button("Login"):
            st.session_state.page = "login"
            st.rerun()
    with colZ:
        if st.button("Sign Up"):
            st.session_state.page = "signup"
            st.rerun()

    # ---------- HERO ----------
    st.markdown("""
    <div class="hero-title">🤖 Intelligent Jobseeker Engagement Platform</div>
    <p class="hero-subtitle">
        AI-powered resume analysis, recruiter shortlisting & career assistant
    </p>
    <hr>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- FEATURE CARDS ----------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3>📄 Resume Analysis</h3>
            <ul>
                <li>Automatic skill extraction</li>
                <li>Resume strength scoring</li>
                <li>ATS-friendly suggestions</li>
                <li>Role-based evaluation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3> Multi Resume Comparison</h3>
            <ul>
                <li>Upload multiple resumes</li>
                <li>Leaderboard ranking</li>
                <li>Smart shortlisting</li>
                <li>Recruiter insights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="glass-card">
            <h3> AI Career Assistant</h3>
            <ul>
                <li>Jobseeker coaching</li>
                <li>Recruiter evaluation</li>
                <li>Interview preparation</li>
                <li>Resume-based Q&A</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ---------- HOW IT WORKS ----------
    st.markdown("""
    <div class="glass-card">
        <h3> How It Works</h3>
        <ol>
            <li>Sign up or log in</li>
            <li>Upload single or multiple resumes</li>
            <li>Get AI-powered insights & scores</li>
            <li>Chat with AI assistant</li>
            <li>Improve hiring or career outcomes</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ---------- CTA ----------
   
# ================= LOGIN PAGE =================
def login_page():

    st.markdown("<h2 style='text-align:center;'> Login</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    colA, colB, colC = st.columns([1, 2, 1])
    with colB:
        with st.container(border=True):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login", use_container_width=True):
                if authenticate_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.user = username
                    st.session_state.page = "app"
                    st.success("Login successful 🚀")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

            if st.button("⬅ Back to Landing", use_container_width=True):
                st.session_state.page = "landing"
                st.rerun()


# ================= SIGNUP PAGE =================
def signup_page():

    st.markdown("<h2 style='text-align:center;'> Sign Up</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    colA, colB, colC = st.columns([1, 2, 1])
    with colB:
        with st.container(border=True):
            username = st.text_input("Choose Username")
            password = st.text_input("Choose Password", type="password")

            if st.button("Create Account", use_container_width=True):
                ok, msg = create_user(username, password)
                if ok:
                    st.success(msg)
                    st.session_state.page = "login"
                    st.rerun()
                else:
                    st.error(msg)

            if st.button("⬅ Back to Landing", use_container_width=True):
                st.session_state.page = "landing"
                st.rerun()


# ================= ROUTER =================
if st.session_state.page == "landing":
    landing_page()

elif st.session_state.page == "login":
    login_page()

elif st.session_state.page == "signup":
    signup_page()

elif st.session_state.page == "app":
    if st.session_state.authenticated:
        run_main_app()
    else:
        st.session_state.page = "landing"
        st.rerun()