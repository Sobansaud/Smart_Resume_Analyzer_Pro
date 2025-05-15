
import streamlit as st
import os
import time
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go
# from transformers import pipeline
# from fpdf import FPDF
# from dotenv import load_dotenv
# from datetime import datetime

from components.resume_reader import Resume_reader
from components.skill_extractor import Skills
from components.scorer import Score
from components.suggestions import SuggestionGenerator

# ---------- CONFIGURATION ----------
# load_dotenv()
# HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

USERS_FILE = "data/users.csv"
PAYMENTS_FILE = "data/payments.csv"
PREMIUM_USERS_FILE = "data/premium_userss.csv"
os.makedirs("data", exist_ok=True)
for file, columns in [
    (USERS_FILE, ["email", "password"]),
    (PAYMENTS_FILE, ["email", "phone", "account_name", "screenshot_name"]),
    (PREMIUM_USERS_FILE, ["email","status"])
]:
    if not os.path.exists(file):
        pd.DataFrame(columns=columns).to_csv(file, index=False)

# ---------- SESSION STATE ----------
for key, default in {
    'logged_in': False,
    'current_user': "",
    'is_premium': False,
    'show_welcome': True
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="📄 Smart Resume Analyzer", layout="centered")

# ---------- GLOBAL STYLES ----------
st.markdown("""
    <style>
    html, body {
        font-family: 'Segoe UI', sans-serif;
        scroll-behavior: smooth;
    }
    .top-bar {
        background-color: #2E86C1;
        color: white;
        padding: 10px;
        text-align: center;
        font-size: 16px;
        border-bottom: 3px solid #154360;
    }
    .welcome-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 85vh;
        animation: fadeZoom 1s ease-out;
    }

    @keyframes fadeZoom {
        0% {
            opacity: 0;
            transform: scale(0.95) translateY(-20px);
        }
        100% {
            opacity: 1;
            transform: scale(1) translateY(0);
        }
    }

    .welcome-title {
        font-size: 2.2em;
        color: #2E86C1;
        margin-top: 10px;
        margin-bottom: 6px;
    }

    .welcome-subtitle {
        font-size: 1.1em;
        color: #444;
    }
    .stButton > button {
        background-color: #2E86C1;
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        transition: 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #1B4F72;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- TOP BAR ----------
st.markdown('<div class="top-bar">🚀 Empower your career with Smart Resume Analyzer</div>', unsafe_allow_html=True)

# ---------- UPDATED WELCOME ANIMATION ----------
if st.session_state.show_welcome:
    st.markdown("""
        <style>
        .welcome-box {
            animation: fadeInSlide 2s ease;
            text-align: center;
            margin-top: 40px;
        }
        @keyframes fadeInSlide {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="welcome-box">', unsafe_allow_html=True)
    st.image("static/logo.png.png", width=220)
    st.markdown("""
        <h2>👋 Welcome to <span style='color:#2E86C1;'><b>Smart Resume Analyzer</b></span></h2>
        <p style='font-size:16px;'>Level up your career with AI-powered resume optimization!</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    time.sleep(1)
    st.session_state.show_welcome = False
    st.rerun()





# ---------- AUTH UI ----------
def auth_ui():
    st.subheader("🔐 Sign In / Sign Up")
    auth_mode = st.radio("Select Action", ["Sign In", "Sign Up"])
    email = st.text_input("📧 Email")
    password = st.text_input("🔑 Password", type="password")
    users_df = pd.read_csv(USERS_FILE)

    if st.button(auth_mode):
        if auth_mode == "Sign Up":
            if email in users_df["email"].values:
                st.warning("⚠️ User already exists! Please sign in.")
            else:
                pd.DataFrame([[email, password]], columns=["email", "password"]).to_csv(USERS_FILE, mode='a', header=False, index=False)
                st.success("✅ Sign-up successful! Please sign in.")
        elif auth_mode == "Sign In":
            if ((users_df["email"] == email) & (users_df["password"] == password)).any():
                st.session_state.logged_in = True
                st.session_state.current_user = email
                premium_users_df = pd.read_csv(PREMIUM_USERS_FILE)
                st.session_state.is_premium = email in premium_users_df["email"].values
                st.success("🎉 Login successful!")
                st.rerun()
            else:
                st.error("🚫 Invalid login. Try again or sign up first.")

if not st.session_state.logged_in:
    auth_ui()
    st.stop()

# ---------- SIDEBAR ----------
with st.sidebar:
    st.image("static/logo.png.png", width=100)
    st.markdown("### 👤 User Info")
    st.write(f"**Logged in as:** {st.session_state.current_user}")
    
    if st.session_state.is_premium:
        st.success("🌟 Premium User")
    else:
        st.warning("🔓 Free User")

    st.markdown("---")
    if st.button("🚪 Logout"):
        for key in st.session_state.keys():
            st.session_state[key] = False
        st.rerun()


# # ---------- MAIN APP ----------

# premium_users_df = pd.read_csv(PREMIUM_USERS_FILE)
# st.session_state.is_premium = st.session_state.current_user in premium_users_df["email"].values

premium_users_df = pd.read_csv(PREMIUM_USERS_FILE)
user_row = premium_users_df[premium_users_df["email"] == st.session_state.current_user]

if not user_row.empty and user_row.iloc[0]["status"].strip().lower() == "verified":
    st.session_state.is_premium = True
else:
    st.session_state.is_premium = False


# Tabs for the app
tabs = [
    "📘 Resume Preview",
    "📊 Score & Summary",
    "✅ Experience",
    "💡 Suggestions",
    "📌 Skills & Analysis",
    "💎 Premium Features"
]

# Add Premium Tools tab for premium users
if st.session_state.is_premium:
    tabs.append("🌟 Premium Tools")


st.title("📝 Smart Resume Analyzer")


st.image("static/logo.png.png", width=120)
st.markdown("""Upload your resume in PDF format to receive:<br>
✅ <strong>Skills Extracted from Resume</strong><br>
📊 <strong>Resume Optimization Score</strong><br>
💡 <strong>Personalized Improvement Tips</strong>
""", unsafe_allow_html=True)


# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader("📤 Upload Your Resume (PDF)", type=["pdf"])

if uploaded_file:
    st.success(f"Successfully uploaded: {uploaded_file.name}")
    reader = Resume_reader(uploaded_file)
    resume_text = reader.extract_text()

    if resume_text:
        skills_df = pd.read_csv("data/skills.csv")
        all_skills = skills_df["skills"].tolist()

        extractor = Skills(resume_text)
        extractor.load_skills("data/skills.csv")
        found_skills = extractor.extracted_skills()
        skill_counts = Counter(found_skills)

        scorer = Score(found_skills, all_skills)
        score = scorer.calculate()
        feedback = scorer.display_feedback(score)

        suggestor = SuggestionGenerator(found_skills, all_skills)
        suggestions = suggestor.generate_suggestions()

        tab_objs = st.tabs(tabs)

        with tab_objs[0]:
            st.subheader("📘 Resume Preview")
            st.code(resume_text[:2000], language="markdown")

        with tab_objs[1]:
            st.subheader("📊 Resume Score")
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=score,
                title={'text': f"Resume Score: {score}"},
                gauge={'axis': {'range': [None, 100]},
                       'bar': {'color': "lightgreen"},
                       'steps': [{'range': [0, 50], 'color': "red"},
                                 {'range': [50, 75], 'color': "orange"},
                                 {'range': [75, 100], 'color': "green"}]}))
            st.plotly_chart(fig, use_container_width=True)

        with tab_objs[2]:
            st.subheader("🔍 Experience")
            if "project" in resume_text.lower() or "experience" in resume_text.lower():
                st.success("✅ Relevant projects/experience found.")
            else:
                st.warning("❗ Add detailed project or experience descriptions.")

        with tab_objs[3]:
            st.subheader("💡 Suggestions")
            for tip in suggestions["tips"]:
                with st.expander(f"• {tip}"):
                    st.markdown("- Tailor your resume for specific roles.")
                    st.markdown("- Quantify your impact.")
                    st.markdown("- Add certifications/tools.")

        with tab_objs[4]:
            st.subheader("📌 Skills Word Cloud")
            if found_skills:
                wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(found_skills))
                plt.figure(figsize=(10, 5))
                plt.imshow(wordcloud, interpolation="bilinear")
                plt.axis("off")
                st.pyplot(plt)
            else:
                st.warning("No skills detected.")

            st.subheader("📊 Skill Frequency")
            if skill_counts:
                selected_skill = st.selectbox("Select a skill", list(skill_counts.keys()))
                st.write(f"The skill **{selected_skill}** appears **{skill_counts[selected_skill]}** time(s).")

        with tab_objs[5]:
            st.subheader("💎 Premium Features")
            if st.session_state.is_premium:
                st.success("🔓 You already have access to premium tools!")
            else:
                st.markdown("""
                    🚀 Unlock the full potential of this platform by accessing our **Premium Tools** – including AI-powered CV builder, job match prediction, and recruiter scan simulation.
                    <br>
                    To activate your premium access, a one-time fee of <strong style="color:#d35400;"> RS.300 </strong> is required. After payment, your tools will be unlocked and enhanced CV services delivered to your email.

                    <div style="border: 2px solid #ccc; padding: 15px; border-radius: 10px; background-color: #f9f9f9;">
                    <strong>📱 Easypaisa:</strong> 0323-2204085 (Muhammad Noaman Saud)<br>
                    <strong>💳 JazzCash:</strong> 0323-2204085 (Muhammad Noaman Saud)
                    </div>
                    """, unsafe_allow_html=True)



                st.subheader("📥 Submit Payment Details")
                phone = st.text_input("📱 Phone Number used for payment")
                account_name = st.text_input("👤 Account Holder Name")
                screenshot = st.file_uploader("📸 Upload Transaction Screenshot", type=["png", "jpg", "jpeg"])

                if st.button("Submit Payment Details"):
                    if phone and account_name and screenshot:
                        payment_df = pd.DataFrame([[st.session_state.current_user, phone, account_name, screenshot.name]],
                                                  columns=["email", "phone", "account_name", "screenshot_name"])
                        payment_df.to_csv(PAYMENTS_FILE, mode='a', header=False, index=False)
                        st.success("✅ Payment details submitted. We will verify and unlock premium features soon.")
                    else:
                        st.error("❗ Please fill all fields and upload screenshot.")

        if st.session_state.is_premium and len(tab_objs) > 6:
            with tab_objs[6]:
                st.subheader("🌟 Premium Tools")

                st.markdown("""
                Unlock the full power of Smart Resume Analyzer with our exclusive premium features designed to supercharge your job hunt!
                """, unsafe_allow_html=True)

                st.markdown("""
                ### 🚀 What You'll Get:
                - 🧠 **AI CV Generator**: Get a polished CV written by artificial intelligence tailored to your field.
                - 📝 **PDF Resume Designer**: Download premium-styled resume templates with personalized feedback.
                - 🔍 **Job Match Predictor**: Discover jobs that align with your profile instantly.
                - 🎯 **ATS Score Analyzer**: Learn how your resume performs with Applicant Tracking Systems.
                - 🕵️‍♂️ **Recruiter Scan Simulator**: Simulate how a recruiter reads and ranks your resume.
                - 💡 **Auto Suggestion Engine**: Get AI-backed suggestions to enhance your content.

                ---
                ✅ Your AI-enhanced CV will be emailed to your registered address automatically.

                🧩 We are constantly updating—more tools coming soon in your Premium Dashboard!
                """, unsafe_allow_html=True)

                st.info("You're already verified for premium access. Enjoy these tools and stay tuned for updates!")


