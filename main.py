
# import streamlit as st
# import os
# import time
# import pandas as pd
# from collections import Counter
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
# from components.ai_cv_generator import generate_cv_cohere_chat
# import plotly.graph_objects as go
# # from transformers import pipeline
# # from fpdf import FPDF
# from dotenv import load_dotenv
# # from datetime import datetime

# from components.resume_reader import Resume_reader
# from components.skill_extractor import Skills
# from components.scorer import Score
# from components.suggestions import SuggestionGenerator

# # ---------- CONFIGURATION ----------
# load_dotenv()
# # HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# USERS_FILE = "data/users.csv"
# PAYMENTS_FILE = "data/payments.csv"
# PREMIUM_USERS_FILE = "data/premium_userss.csv"
# os.makedirs("data", exist_ok=True)
# for file, columns in [
#     (USERS_FILE, ["email", "password"]),
#     (PAYMENTS_FILE, ["email", "phone", "account_name", "screenshot_name"]),
#     (PREMIUM_USERS_FILE, ["email","status"])
# ]:
#     if not os.path.exists(file):
#         pd.DataFrame(columns=columns).to_csv(file, index=False)

# # ---------- SESSION STATE ----------
# for key, default in {
#     'logged_in': False,
#     'current_user': "",
#     'is_premium': False,
#     'show_welcome': True
# }.items():
#     if key not in st.session_state:
#         st.session_state[key] = default

# # ---------- PAGE CONFIG ----------
# st.set_page_config(page_title="📄 Smart Resume Analyzer", layout="centered")

# # ---------- GLOBAL STYLES ----------
# st.markdown("""
#     <style>
#     html, body {
#         font-family: 'Segoe UI', sans-serif;
#         scroll-behavior: smooth;
#     }
#     .top-bar {
#         background-color: #2E86C1;
#         color: white;
#         padding: 10px;
#         text-align: center;
#         font-size: 16px;
#         border-bottom: 3px solid #154360;
#     }
#     .welcome-container {
#         display: flex;
#         flex-direction: column;
#         align-items: center;
#         justify-content: center;
#         height: 85vh;
#         animation: fadeZoom 1s ease-out;
#     }

#     @keyframes fadeZoom {
#         0% {
#             opacity: 0;
#             transform: scale(0.95) translateY(-20px);
#         }
#         100% {
#             opacity: 1;
#             transform: scale(1) translateY(0);
#         }
#     }

#     .welcome-title {
#         font-size: 2.2em;
#         color: #2E86C1;
#         margin-top: 10px;
#         margin-bottom: 6px;
#     }

#     .welcome-subtitle {
#         font-size: 1.1em;
#         color: #444;
#     }
#     .stButton > button {
#         background-color: #2E86C1;
#         color: white;
#         border-radius: 0.5rem;
#         padding: 0.5rem 1rem;
#         transition: 0.3s ease;
#     }
#     .stButton > button:hover {
#         background-color: #1B4F72;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # ---------- TOP BAR ----------
# st.markdown('<div class="top-bar">🚀 Empower your career with Smart Resume Analyzer</div>', unsafe_allow_html=True)

# # ---------- UPDATED WELCOME ANIMATION ----------
# if st.session_state.show_welcome:
#     st.markdown("""
#         <style>
#         .welcome-box {
#             animation: fadeInSlide 2s ease;
#             text-align: center;
#             margin-top: 40px;
#         }
#         @keyframes fadeInSlide {
#             from {
#                 opacity: 0;
#                 transform: translateY(-30px);
#             }
#             to {
#                 opacity: 1;
#                 transform: translateY(0);
#             }
#         }
#         </style>
#     """, unsafe_allow_html=True)

#     st.markdown('<div class="welcome-box">', unsafe_allow_html=True)
#     st.image("static/logo.png.png", width=220)
#     st.markdown("""
#         <h2>👋 Welcome to <span style='color:#2E86C1;'><b>Smart Resume Analyzer</b></span></h2>
#         <p style='font-size:16px;'>Level up your career with AI-powered resume optimization!</p>
#     """, unsafe_allow_html=True)
#     st.markdown('</div>', unsafe_allow_html=True)

#     time.sleep(1)
#     st.session_state.show_welcome = False
#     st.rerun()





# # ---------- AUTH UI ----------
# def auth_ui():
#     st.subheader("🔐 Sign In / Sign Up")
#     auth_mode = st.radio("Select Action", ["Sign In", "Sign Up"])
#     email = st.text_input("📧 Email")
#     password = st.text_input("🔑 Password", type="password")
#     users_df = pd.read_csv(USERS_FILE)

#     if st.button(auth_mode):
#         if auth_mode == "Sign Up":
#             if email in users_df["email"].values:
#                 st.warning("⚠️ User already exists! Please sign in.")
#             else:
#                 pd.DataFrame([[email, password]], columns=["email", "password"]).to_csv(USERS_FILE, mode='a', header=False, index=False)
#                 st.success("✅ Sign-up successful! Please sign in.")
#         elif auth_mode == "Sign In":
#             if ((users_df["email"] == email) & (users_df["password"] == password)).any():
#                 st.session_state.logged_in = True
#                 st.session_state.current_user = email
#                 premium_users_df = pd.read_csv(PREMIUM_USERS_FILE)
#                 st.session_state.is_premium = email in premium_users_df["email"].values
#                 st.success("🎉 Login successful!")
#                 st.rerun()
#             else:
#                 st.error("🚫 Invalid login. Try again or sign up first.")

# if not st.session_state.logged_in:
#     auth_ui()
#     st.stop()

# # ---------- SIDEBAR ----------
# with st.sidebar:
#     st.image("static/logo.png.png", width=100)
#     st.markdown("### 👤 User Info")
#     st.write(f"**Logged in as:** {st.session_state.current_user}")
    
#     if st.session_state.is_premium:
#         st.success("🌟 Premium User")
#     else:
#         st.warning("🔓 Free User")

#     st.markdown("---")
#     if st.button("🚪 Logout"):
#         for key in st.session_state.keys():
#             st.session_state[key] = False
#         st.rerun()


# # # ---------- MAIN APP ----------

# # premium_users_df = pd.read_csv(PREMIUM_USERS_FILE)
# # st.session_state.is_premium = st.session_state.current_user in premium_users_df["email"].values

# premium_users_df = pd.read_csv(PREMIUM_USERS_FILE)
# user_row = premium_users_df[premium_users_df["email"] == st.session_state.current_user]

# # if not user_row.empty and user_row.iloc[0]["status"].strip().lower() == "verified":
# #     st.session_state.is_premium = True
# # else:
# #     st.session_state.is_premium = False
# if not user_row.empty:
#     status_value = user_row.iloc[0]["status"]
#     if isinstance(status_value, str) and status_value.strip().lower() == "verified":
#         st.session_state.is_premium = True
#     else:
#         st.session_state.is_premium = False
# else:
#     st.session_state.is_premium = False



# # Tabs for the app
# tabs = [
#     "📘 Resume Preview",
#     "📊 Score & Summary",
#     "✅ Experience",
#     "💡 Suggestions",
#     "📌 Skills & Analysis",
#     "💎 Premium Features"
# ]

# # Add Premium Tools tab for premium users
# if st.session_state.is_premium:
#     tabs.append("🌟 Premium Tools")


# st.title("📝 Smart Resume Analyzer")


# st.image("static/logo.png.png", width=120)
# st.markdown("""Upload your resume in PDF format to receive:<br>
# ✅ <strong>Skills Extracted from Resume</strong><br>
# 📊 <strong>Resume Optimization Score</strong><br>
# 💡 <strong>Personalized Improvement Tips</strong>
# """, unsafe_allow_html=True)


# # ---------- FILE UPLOAD ----------
# uploaded_file = st.file_uploader("📤 Upload Your Resume (PDF)", type=["pdf"])

# if uploaded_file:
#     st.success(f"Successfully uploaded: {uploaded_file.name}")
#     reader = Resume_reader(uploaded_file)
#     resume_text = reader.extract_text()

#     if resume_text:
#         skills_df = pd.read_csv("data/skills.csv")
#         all_skills = skills_df["skills"].tolist()

#         extractor = Skills(resume_text)
#         extractor.load_skills("data/skills.csv")
#         found_skills = extractor.extracted_skills()
#         skill_counts = Counter(found_skills)

#         scorer = Score(found_skills, all_skills)
#         score = scorer.calculate()
#         feedback = scorer.display_feedback(score)

#         suggestor = SuggestionGenerator(found_skills, all_skills)
#         suggestions = suggestor.generate_suggestions()

#         tab_objs = st.tabs(tabs)

#         with tab_objs[0]:
#             st.subheader("📘 Resume Preview")
#             st.code(resume_text[:2000], language="markdown")

#         with tab_objs[1]:
#             st.subheader("📊 Resume Score")
#             fig = go.Figure(go.Indicator(
#                 mode="gauge+number", value=score,
#                 title={'text': f"Resume Score: {score}"},
#                 gauge={'axis': {'range': [None, 100]},
#                        'bar': {'color': "lightgreen"},
#                        'steps': [{'range': [0, 50], 'color': "red"},
#                                  {'range': [50, 75], 'color': "orange"},
#                                  {'range': [75, 100], 'color': "green"}]}))
#             st.plotly_chart(fig, use_container_width=True)

#         with tab_objs[2]:
#             st.subheader("🔍 Experience")
#             if "project" in resume_text.lower() or "experience" in resume_text.lower():
#                 st.success("✅ Relevant projects/experience found.")
#             else:
#                 st.warning("❗ Add detailed project or experience descriptions.")

#         with tab_objs[3]:
#             st.subheader("💡 Suggestions")
#             for tip in suggestions["tips"]:
#                 with st.expander(f"• {tip}"):
#                     st.markdown("- Tailor your resume for specific roles.")
#                     st.markdown("- Quantify your impact.")
#                     st.markdown("- Add certifications/tools.")

#         with tab_objs[4]:
#             st.subheader("📌 Skills Word Cloud")
#             if found_skills:
#                 wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(found_skills))
#                 plt.figure(figsize=(10, 5))
#                 plt.imshow(wordcloud, interpolation="bilinear")
#                 plt.axis("off")
#                 st.pyplot(plt)
#             else:
#                 st.warning("No skills detected.")

#             st.subheader("📊 Skill Frequency")
#             if skill_counts:
#                 selected_skill = st.selectbox("Select a skill", list(skill_counts.keys()))
#                 st.write(f"The skill **{selected_skill}** appears **{skill_counts[selected_skill]}** time(s).")

#         with tab_objs[5]:
#             st.subheader("💎 Premium Features")
#             if st.session_state.is_premium:
#                 st.success("🔓 You already have access to premium tools!")
#             else:
#                 st.markdown("""
#                     🚀 Unlock the full potential of this platform by accessing our **Premium Tools** – including AI-powered CV builder, job match prediction, and recruiter scan simulation.
#                     <br>
#                     To activate your premium access, a one-time fee of <strong style="color:#d35400;"> RS.300 </strong> is required. After payment, your tools will be unlocked and enhanced CV services delivered to your email.

#                     <div style="border: 2px solid #ccc; padding: 15px; border-radius: 10px; background-color: #f9f9f9;">
#                     <strong>📱 Easypaisa:</strong> 0323-2204085 (Muhammad Noaman Saud)<br>
#                     <strong>💳 JazzCash:</strong> 0323-2204085 (Muhammad Noaman Saud)
#                     </div>
#                     """, unsafe_allow_html=True)



#                 st.subheader("📥 Submit Payment Details")
#                 phone = st.text_input("📱 Phone Number used for payment")
#                 account_name = st.text_input("👤 Account Holder Name")
#                 screenshot = st.file_uploader("📸 Upload Transaction Screenshot", type=["png", "jpg", "jpeg"])

#                 if st.button("Submit Payment Details"):
#                     if phone and account_name and screenshot:
#                         payment_df = pd.DataFrame([[st.session_state.current_user, phone, account_name, screenshot.name]],
#                                                   columns=["email", "phone", "account_name", "screenshot_name"])
#                         payment_df.to_csv(PAYMENTS_FILE, mode='a', header=False, index=False)
#                         st.success("✅ Payment details submitted. We will verify and unlock premium features soon.")
#                     else:
#                         st.error("❗ Please fill all fields and upload screenshot.")

#         if st.session_state.is_premium and len(tab_objs) > 6:
#             with tab_objs[6]:
#                 st.subheader("🌟 Premium Tools")

#                 st.markdown("""
#                 Unlock the full power of Smart Resume Analyzer with our exclusive premium features designed to supercharge your job hunt!
#                 """, unsafe_allow_html=True)

#                 st.markdown("""
#                 ### 🚀 What You'll Get:
#                 - 🧠 **AI CV Generator**: Get a polished CV written by artificial intelligence tailored to your field.
#                 - 📝 **PDF Resume Designer**: Download premium-styled resume templates with personalized feedback.
#                 - 🔍 **Job Match Predictor**: Discover jobs that align with your profile instantly.
#                 - 🎯 **ATS Score Analyzer**: Learn how your resume performs with Applicant Tracking Systems.
#                 - 🕵️‍♂️ **Recruiter Scan Simulator**: Simulate how a recruiter reads and ranks your resume.
#                 - 💡 **Auto Suggestion Engine**: Get AI-backed suggestions to enhance your content.

#                 ---
#                 ✅ Your AI-enhanced CV will be emailed to your registered address automatically.

#                 🧩 We are constantly updating—more tools coming soon in your Premium Dashboard!
#                 """, unsafe_allow_html=True)
                
#         st.subheader("✍️ Fill the form to generate your CV")
#         name = st.text_input("Full Name")
#         education = st.text_area("Education")
#         email = st.text_input("Email")
#         experience = st.text_area("Work Experience")
#         skills = st.text_area("Skills")
#         interests = st.text_area("Interests")

#         st.markdown("### ✨ Generate AI CV using Cohere")

#         if st.button("Generate CV using Cohere Chat"):
#             if name and email and education and experience and skills and interests:
#                 with st.spinner("Generating your professional CV..."):
#                     cv_result = generate_cv_cohere_chat(name, email, education, experience, skills, interests)
#             if cv_result.startswith("❌"):
#                 st.error(cv_result)
#             else:
#                 st.success("✅ CV Generated!")
#                 st.subheader("📝 Your AI CV:")
#                 st.code(cv_result, language="markdown")
#         else:
#             st.error("⚠️ Please fill in all fields before generating the CV.")
#             st.info("You're already verified for premium access. Enjoy these tools and stay tuned for updates!")




import streamlit as st
import os
import time
import pandas as pd
from collections import Counter
import jinja2
import stripe
# from xhtml2pdf import pisa
# from jinja2 import Environment, FileSystemLoader
import io
from wordcloud import WordCloud
import unicodedata
import matplotlib.pyplot as plt
from components.ai_cv_generator import generate_cv_cohere_chat
import plotly.graph_objects as go
from dotenv import load_dotenv
from fpdf import FPDF
from io import BytesIO
import base64
import streamlit.components.v1 as components
from components.resume_reader import Resume_reader
from components.skill_extractor import Skills
from components.scorer import Score
from components.suggestions import SuggestionGenerator

# ---------- CONFIGURATION ----------
load_dotenv()



# from fpdf import FPDF
# import os
# from io import BytesIO
# import unicodedata

# def clean_text(text):
#     try:
#         if isinstance(text, list):
#             text = ", ".join(map(str, text))
#         return unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode("ascii")
#     except Exception:
#         return str(text) or ""

# def render_pdf_from_data(context):
#     pdf = FPDF()
#     pdf.add_page()
#     epw = pdf.w - 2 * pdf.l_margin

#     # Load font
#     font_path = os.path.join(os.path.dirname(__file__), 'DejaVuSans.ttf')
#     if not os.path.isfile(font_path):
#         raise FileNotFoundError(f"Font file not found: {font_path}")
#     pdf.add_font('DejaVu', '', font_path, uni=True)
#     pdf.set_font('DejaVu', '', 20)

#     # Name
#     pdf.cell(0, 15, txt=clean_text(context.get("name", "Name")), ln=True, align="C")

#     # Email
#     pdf.set_font('DejaVu', '', 12)
#     pdf.cell(0, 10, txt=f"Email: {clean_text(context.get('email', ''))}", ln=True, align="C")
#     pdf.ln(10)

#     def add_section(title, content):
#         if content:
#             pdf.set_font('DejaVu', '', 14)
#             pdf.cell(0, 10, f"{title}:", ln=True)
#             pdf.set_font('DejaVu', '', 12)
#             text = clean_text(content)
#             pdf.multi_cell(epw, 8, text)
#             pdf.ln(5)

#     # About Me
#     add_section("About Me", context.get("about_me", ""))

#     # Skills
#     add_section("Skills", context.get("skills", []))

#     # Education
#     add_section("Education", context.get("education", []))

#     # Experience
#     add_section("Experience", context.get("experience", []))

#     # Projects
#     add_section("Projects", context.get("projects", []))

#     # Interests
#     add_section("Interests", context.get("interests", []))

#     # Social Links
#     links = []
#     for platform in ["linkedin", "github", "twitter"]:
#         link = context.get(platform, "")
#         if link:
#             links.append(f"{platform.capitalize()}: {link}")
#     add_section("Social Links", links)

#     pdf_output = pdf.output(dest='S').encode('latin1', 'ignore')
#     return BytesIO(pdf_output)


# from fpdf import FPDF
# import os
# from io import BytesIO
# import unicodedata

# def clean_text(text):
#     try:
#         if isinstance(text, list):
#             return "\n".join(map(lambda s: "- " + str(s).strip(), text))  # List into bullet style
#         return unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode("ascii")
#     except Exception:
#         return str(text) or ""

# def render_pdf_from_data(context):
#     pdf = FPDF()
#     pdf.add_page()
#     epw = pdf.w - 2 * pdf.l_margin

#     # Font setup
#     font_path = os.path.join(os.path.dirname(__file__), 'DejaVuSans.ttf')
#     if not os.path.isfile(font_path):
#         raise FileNotFoundError(f"Font file not found: {font_path}")
#     pdf.add_font('DejaVu', '', font_path, uni=True)

#     # Name & Email
#     pdf.set_font('DejaVu', '', 20)
#     pdf.cell(0, 15, txt=clean_text(context.get("name", "John Doe")), ln=True, align="C")

#     pdf.set_font('DejaVu', '', 12)
#     pdf.cell(0, 10, txt=f"Email: {clean_text(context.get('email', 'johndoe@example.com'))}", ln=True, align="C")
#     pdf.ln(8)

#     def add_section(title, content, is_list=False):
#         if content:
#             pdf.set_font('DejaVu', '', 14)
#             pdf.cell(0, 10, f"{title}:", ln=True)
#             pdf.set_font('DejaVu', '', 12)
#             if is_list and isinstance(content, list):
#                 for item in content:
#                     pdf.multi_cell(epw, 8, f"- {clean_text(item)}")
#             else:
#                 pdf.multi_cell(epw, 8, clean_text(content))
#             pdf.ln(4)

#     # About Me - paragraph style
#     about_me = context.get("about_me", "A motivated and detail-oriented professional with a passion for solving real-world problems using technology.")
#     add_section("About Me", about_me)

#     # Skills - bulleted
#     skills = context.get("skills", ["Python", "FastAPI", "Next.js", "Machine Learning", "Git"])
#     add_section("Skills", skills, is_list=True)

#     # Education - formatted list
#     education = context.get("education", [
#         "BSc in Computer Science - University of XYZ (2020 - 2024)",
#         "Intermediate in Pre-Engineering - ABC College (2018 - 2020)"
#     ])
#     add_section("Education", education, is_list=True)

#     # Experience - formatted list
#     experience = context.get("experience", [
#         "Software Intern at DevSolutions - Built REST APIs using FastAPI (Jun 2023 - Aug 2023)",
#         "Frontend Developer - Freelance Projects using React and TailwindCSS (2022 - Present)"
#     ])
#     add_section("Experience", experience, is_list=True)

#     # Projects - formatted list
#     projects = context.get("projects", [
#         "Smart Resume Analyzer - An AI-based web app to analyze and enhance resumes.",
#         "E-commerce Dashboard - Built a full-stack dashboard with analytics using Next.js and Django."
#     ])
#     add_section("Projects", projects, is_list=True)

#     # Interests
#     interests = context.get("interests", ["Open Source", "Tech Blogging", "Hackathons"])
#     add_section("Interests", interests, is_list=True)

#     # Social Links
#     links = []
#     for platform in ["linkedin", "github", "twitter"]:
#         link = context.get(platform)
#         if link:
#             links.append(f"{platform.capitalize()}: {link}")
#     add_section("Social Links", links, is_list=True)

#     # Final output
#     pdf_output = pdf.output(dest='S').encode('latin1', 'ignore')
#     return BytesIO(pdf_output)



# from fpdf import FPDF
# import os
# from io import BytesIO
# import unicodedata

# def clean_text(text):
#     try:
#         if isinstance(text, list):
#             return "\n".join(map(lambda s: "- " + str(s).strip(), text))
#         return unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode("ascii")
#     except Exception:
#         return str(text) or ""

# def render_pdf_from_data(context):
#     pdf = FPDF()
#     pdf.add_page()

#     # Fonts
#     font_path = os.path.join(os.path.dirname(__file__), 'DejaVuSans.ttf')
#     if not os.path.isfile(font_path):
#         raise FileNotFoundError(f"Font file not found: {font_path}")
#     pdf.add_font('DejaVu', '', font_path, uni=True)

#     pdf.set_font('DejaVu', '', 20)
#     pdf.set_text_color(30, 30, 30)
#     pdf.cell(0, 15, txt=clean_text(context.get("name", "John Doe")), ln=True, align="C")

#     pdf.set_font('DejaVu', '', 12)
#     pdf.set_text_color(100, 100, 100)
#     pdf.cell(0, 10, txt=f"Email: {clean_text(context.get('email', 'johndoe@example.com'))}", ln=True, align="C")
#     pdf.ln(10)

#     # Define column widths
#     page_width = pdf.w - 20
#     left_col_width = page_width * 0.4
#     right_col_width = page_width * 0.6
#     margin_left = 10
#     margin_top = pdf.get_y()
#     line_height = 6

#     def add_section(x, y, w, title, content, is_list=False):
#         pdf.set_xy(x, y)
#         pdf.set_font('DejaVu', '', 14)
#         pdf.set_text_color(0, 0, 80)
#         pdf.cell(w, 10, txt=title, ln=True)

#         pdf.set_font('DejaVu', '', 11)
#         pdf.set_text_color(0, 0, 0)
#         if is_list and isinstance(content, list):
#             for item in content:
#                 pdf.set_x(x)
#                 pdf.multi_cell(w, line_height, f"• {clean_text(item)}")
#         else:
#             pdf.set_x(x)
#             pdf.multi_cell(w, line_height, clean_text(content))
#         pdf.ln(2)
#         return pdf.get_y()

#     # Starting y position
#     y_left = margin_top
#     y_right = margin_top

#     # LEFT COLUMN
#     y_left = add_section(margin_left, y_left, left_col_width, "About Me", context.get("about_me", "Enthusiastic developer..."))
#     y_left = add_section(margin_left, y_left, left_col_width, "Skills", context.get("skills", []), is_list=True)
#     y_left = add_section(margin_left, y_left, left_col_width, "Interests", context.get("interests", []), is_list=True)

#     links = []
#     for platform in ["linkedin", "github", "twitter"]:
#         link = context.get(platform)
#         if link:
#             links.append(f"{platform.capitalize()}: {link}")
#     y_left = add_section(margin_left, y_left, left_col_width, "Social Links", links, is_list=True)

#     # RIGHT COLUMN
#     x_right = margin_left + left_col_width + 10
#     y_right = add_section(x_right, margin_top, right_col_width, "Education", context.get("education", []), is_list=True)
#     y_right = add_section(x_right, y_right, right_col_width, "Experience", context.get("experience", []), is_list=True)
#     y_right = add_section(x_right, y_right, right_col_width, "Projects", context.get("projects", []), is_list=True)

#     # Output
#     return BytesIO(pdf.output(dest='S').encode('latin1', 'ignore'))



# from fpdf import FPDF
# import os
# from io import BytesIO
# import unicodedata

# def clean_text(text):
#     try:
#         if isinstance(text, list):
#             return "\n".join(map(lambda s: "- " + str(s).strip(), text))
#         return unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode("ascii")
#     except Exception:
#         return str(text) or ""

# def render_pdf_from_data(context):
#     pdf = FPDF()
#     pdf.add_page()

#     # Fonts
#     font_path = os.path.join(os.path.dirname(__file__), 'DejaVuSans.ttf')
#     if not os.path.isfile(font_path):
#         raise FileNotFoundError(f"Font file not found: {font_path}")
#     pdf.add_font('DejaVu', '', font_path, uni=True)

#     pdf.set_font('DejaVu', '', 20)
#     pdf.set_text_color(30, 30, 30)
#     pdf.cell(0, 15, txt=clean_text(context.get("name", "John Doe")), ln=True, align="C")

#     pdf.set_font('DejaVu', '', 12)
#     pdf.set_text_color(100, 100, 100)
#     pdf.cell(0, 10, txt=f"Email: {clean_text(context.get('email', 'johndoe@example.com'))}", ln=True, align="C")
#     pdf.ln(5)

#     # Optional profile image
#     image_path = os.path.join("static", "profile.jpg")
#     if os.path.isfile(image_path):
#         pdf.image(image_path, x=10, y=pdf.get_y(), w=30)
#         pdf.ln(35)
#     else:
#         pdf.ln(10)

#     # Layout dimensions
#     page_width = pdf.w - 20
#     left_col_width = page_width * 0.4
#     right_col_width = page_width * 0.6
#     margin_left = 10
#     x_right = margin_left + left_col_width + 10
#     y_start = pdf.get_y()
#     line_height = 6

#     # Draw center line
#     center_x = margin_left + left_col_width + 5
#     pdf.set_draw_color(200, 200, 200)
#     pdf.line(center_x, y_start - 5, center_x, 280)

#     def add_section(x, y, w, title, content, is_list=False):
#         pdf.set_xy(x, y)
#         pdf.set_font('DejaVu', '', 13)
#         pdf.set_text_color(0, 0, 100)
#         pdf.cell(w, 8, txt=title, ln=True)

#         pdf.set_font('DejaVu', '', 11)
#         pdf.set_text_color(30, 30, 30)
#         if is_list and isinstance(content, list):
#             for item in content:
#                 pdf.set_x(x)
#                 pdf.multi_cell(w, line_height, f"• {clean_text(item)}")
#         else:
#             pdf.set_x(x)
#             pdf.multi_cell(w, line_height, clean_text(content))
#         pdf.ln(2)
#         return pdf.get_y()

#     # LEFT COLUMN
#     y_left = y_start
#     y_left = add_section(margin_left, y_left, left_col_width, "About Me", context.get("about_me", "A passionate developer..."))
#     y_left = add_section(margin_left, y_left, left_col_width, "Skills", context.get("skills", []), is_list=True)
#     y_left = add_section(margin_left, y_left, left_col_width, "Interests", context.get("interests", []), is_list=True)

#     links = []
#     for platform in ["linkedin", "github", "twitter"]:
#         link = context.get(platform)
#         if link:
#             links.append(f"{platform.capitalize()}: {link}")
#     y_left = add_section(margin_left, y_left, left_col_width, "Social Links", links, is_list=True)

#     # RIGHT COLUMN
#     y_right = y_start
#     y_right = add_section(x_right, y_right, right_col_width, "Education", context.get("education", []), is_list=True)
#     y_right = add_section(x_right, y_right, right_col_width, "Experience", context.get("experience", []), is_list=True)
#     y_right = add_section(x_right, y_right, right_col_width, "Projects", context.get("projects", []), is_list=True)

#     # Output as BytesIO
#     return BytesIO(pdf.output(dest='S').encode('latin1', 'ignore'))


# from fpdf import FPDF
# from io import BytesIO
# import os
# import base64
# import unicodedata
# from PIL import Image
# from tempfile import NamedTemporaryFile


# def clean_text(text):
#     try:
#         if isinstance(text, list):
#             return "\n".join(map(lambda s: "• " + str(s).strip(), text))
#         return unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode("ascii")
#     except Exception:
#         return str(text) or ""


# def render_pdf_from_data(context):
#     pdf = FPDF()
#     pdf.add_page()
#     epw = pdf.w - 2 * pdf.l_margin
#     col_width = epw / 2 - 5

#     # Font setup
#     font_path = os.path.join(os.path.dirname(__file__), 'DejaVuSans.ttf')
#     if not os.path.isfile(font_path):
#         raise FileNotFoundError(f"Font file not found: {font_path}")
#     pdf.add_font('DejaVu', '', font_path, uni=True)

#     pdf.set_font('DejaVu', '', 12)

#     # === Profile Image ===
#     image_url = context.get("profile_image_url", "")
#     if image_url.startswith("data:image"):
#         try:
#             header, encoded = image_url.split(",", 1)
#             img_bytes = base64.b64decode(encoded)
#             img = Image.open(BytesIO(img_bytes))

#             with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
#                 img.save(tmpfile.name)
#                 pdf.image(tmpfile.name, x=pdf.w / 2 - 20, y=10, w=40, h=40)
#                 os.unlink(tmpfile.name)
#             pdf.ln(45)
#         except Exception as e:
#             print("Error adding image:", e)
#             pdf.ln(10)
#     else:
#         pdf.ln(10)

#     # === Name and Email Centered ===
#     pdf.set_font('DejaVu', '', 20)
#     pdf.cell(0, 10, clean_text(context.get("name", "John Doe")), ln=True, align="C")

#     pdf.set_font('DejaVu', '', 12)
#     pdf.cell(0, 8, f"Email: {clean_text(context.get('email', 'johndoe@example.com'))}", ln=True, align="C")
#     pdf.ln(8)

#     # === Divider Line ===
#     line_y = pdf.get_y()
#     pdf.set_draw_color(150, 150, 150)
#     pdf.set_line_width(0.3)
#     pdf.line(pdf.l_margin + epw / 2, line_y, pdf.l_margin + epw / 2, 280)  # Vertical line

#     # === Two-Column Section Helper ===
#     def add_section(title, content, is_list=False, left=True):
#         x = pdf.l_margin if left else pdf.l_margin + epw / 2 + 5
#         y = pdf.get_y()
#         pdf.set_xy(x, y)
#         pdf.set_font('DejaVu', '', 14)
#         pdf.cell(col_width, 8, f"{title}:", ln=True)
#         pdf.set_font('DejaVu', '', 11)
#         pdf.set_x(x)
#         if is_list and isinstance(content, list):
#             for item in content:
#                 pdf.multi_cell(col_width, 6, f"• {clean_text(item)}")
#                 pdf.set_x(x)
#         else:
#             pdf.multi_cell(col_width, 6, clean_text(content))
#         pdf.ln(2)

#     # === Split Sections ===
#     # Left Column
#     add_section("About Me", context.get("about_me", ""), left=True)
#     add_section("Skills", context.get("skills", "").split("\n"), is_list=True, left=True)
#     add_section("Education", context.get("education", "").split("\n"), is_list=True, left=True)
#     add_section("Projects", context.get("projects", []), is_list=True, left=True)

#     # Right Column
#     add_section("Experience", context.get("experience", "").split("\n"), is_list=True, left=False)
#     add_section("Interests", context.get("interests", "").split("\n"), is_list=True, left=False)

#     # Social Links
#     links = []
#     for platform in ["linkedin", "github", "twitter"]:
#         link = context.get(platform)
#         if link:
#             links.append(f"{platform.capitalize()}: {link}")
#     add_section("Social Links", links, is_list=True, left=False)

#     # Output as PDF in memory
#     pdf_output = pdf.output(dest='S').encode('latin1', 'ignore')
#     return BytesIO(pdf_output)


# from fpdf import FPDF
# from io import BytesIO
# import os
# import base64
# import unicodedata
# from PIL import Image
# from tempfile import NamedTemporaryFile


# def clean_text(text):
#     try:
#         if isinstance(text, list):
#             return "\n".join(map(lambda s: "• " + str(s).strip(), text))
#         return unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode("ascii")
#     except Exception:
#         return str(text) or ""


# def render_pdf_from_data(context):
#     pdf = FPDF()
#     pdf.set_auto_page_break(False)  # Manual control
#     pdf.add_page()

#     epw = pdf.w - 2 * pdf.l_margin
#     col_width = epw / 2 - 5

#     # Font
#     font_path = os.path.join(os.path.dirname(__file__), 'DejaVuSans.ttf')
#     if not os.path.isfile(font_path):
#         raise FileNotFoundError(f"Font file not found: {font_path}")
#     pdf.add_font('DejaVu', '', font_path, uni=True)
#     pdf.set_font('DejaVu', '', 12)

#     # === Image ===
#     image_url = context.get("profile_image_url", "")
#     if image_url.startswith("data:image"):
#         try:
#             header, encoded = image_url.split(",", 1)
#             img_bytes = base64.b64decode(encoded)
#             img = Image.open(BytesIO(img_bytes))
#             with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
#                 img.save(tmpfile.name)
#                 pdf.image(tmpfile.name, x=pdf.w / 2 - 20, y=10, w=40, h=40)
#                 os.unlink(tmpfile.name)
#         except:
#             pass
#     pdf.ln(45)

#     # === Name and Email ===
#     pdf.set_font('DejaVu', '', 20)
#     pdf.cell(0, 10, clean_text(context.get("name", "John Doe")), ln=True, align="C")
#     pdf.set_font('DejaVu', '', 12)
#     pdf.cell(0, 8, f"Email: {clean_text(context.get('email', 'johndoe@example.com'))}", ln=True, align="C")
#     pdf.ln(6)

#     # === Column Separation Line ===
#     top_y = pdf.get_y()
#     bottom_y = 280
#     pdf.set_draw_color(180, 180, 180)
#     pdf.set_line_width(0.3)
#     pdf.line(pdf.l_margin + epw / 2, top_y, pdf.l_margin + epw / 2, bottom_y)

#     # === Data ===
#     left_sections = [
#         ("About Me", context.get("about_me", ""), False),
#         ("Skills", context.get("skills", "").split("\n"), True),
#         ("Education", context.get("education", "").split("\n"), True),
#         ("Projects", context.get("projects", []), True),
#     ]

#     right_sections = [
#         ("Experience", context.get("experience", "").split("\n"), True),
#         ("Interests", context.get("interests", "").split("\n"), True),
#         ("Social Links", [
#             f"{p.capitalize()}: {context.get(p)}"
#             for p in ["linkedin", "github", "twitter"] if context.get(p)
#         ], True),
#     ]

#     y_left = pdf.get_y()
#     y_right = y_left
#     x_left = pdf.l_margin
#     x_right = pdf.l_margin + epw / 2 + 5

#     def draw_section(x, y, title, content, is_list):
#         pdf.set_xy(x, y)
#         pdf.set_font('DejaVu', '', 14)
#         pdf.cell(col_width, 8, f"{title}:", ln=True)
#         pdf.set_font('DejaVu', '', 11)
#         start_y = pdf.get_y()
#         pdf.set_x(x)

#         if is_list and isinstance(content, list):
#             for item in content:
#                 pdf.set_x(x)
#                 pdf.multi_cell(col_width, 6, f"• {clean_text(item)}")
#         else:
#             pdf.multi_cell(col_width, 6, clean_text(content))

#         return pdf.get_y() + 2

#     # Left column
#     for title, content, is_list in left_sections:
#         y_left = draw_section(x_left, y_left, title, content, is_list)

#     # Right column
#     for title, content, is_list in right_sections:
#         y_right = draw_section(x_right, y_right, title, content, is_list)

#     pdf_output = pdf.output(dest='S').encode('latin1', 'ignore')
#     return BytesIO(pdf_output)
from fpdf import FPDF
from io import BytesIO
import os
import base64
import unicodedata
from PIL import Image
from tempfile import NamedTemporaryFile

def clean_text(text):
    try:
        if isinstance(text, list):
            return "\n".join(map(lambda s: "• " + str(s).strip(), text))
        return unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode("ascii")
    except Exception:
        return str(text) or ""

class PDF(FPDF):
    def multi_cell_height(self, w, h, txt):
        # Approximate height of multi_cell for given text
        # Counting number of lines it will take
        # This is an estimate since FPDF doesn't provide it directly
        nb = txt.count('\n') + 1
        # Further split lines that exceed width
        cw = self.get_string_width('A')  # average char width approx
        max_chars_per_line = int(w / cw)
        total_lines = 0
        for line in txt.split('\n'):
            length = len(line)
            lines = length // max_chars_per_line + 1
            total_lines += lines
        return total_lines * h

def render_pdf_from_data(context):
    pdf = PDF()
    pdf.set_auto_page_break(auto=False)  # We manage page breaks ourselves
    pdf.add_page()

    epw = pdf.w - 2 * pdf.l_margin
    col_width = epw / 2 - 5
    page_height = pdf.h - pdf.t_margin - pdf.b_margin

    # Font loading
    font_path = os.path.join(os.path.dirname(__file__), 'DejaVuSans.ttf')
    if not os.path.isfile(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")
    pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.set_font('DejaVu', '', 12)

    # Profile Image
    image_url = context.get("profile_image_url", "")
    if image_url.startswith("data:image"):
        try:
            header, encoded = image_url.split(",", 1)
            img_bytes = base64.b64decode(encoded)
            img = Image.open(BytesIO(img_bytes))
            with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                img.save(tmpfile.name)
                pdf.image(tmpfile.name, x=pdf.w / 2 - 17, y=10, w=34, h=34)
                os.unlink(tmpfile.name)
        except:
            pass
    pdf.ln(40)

    # Name and Email
    pdf.set_font('DejaVu', '', 22)
    pdf.set_text_color(0, 0, 80)
    pdf.cell(0, 12, clean_text(context.get("name", "John Doe")), ln=True, align="C")

    pdf.set_font('DejaVu', '', 13)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, f"Email: {clean_text(context.get('email', 'johndoe@example.com'))}", ln=True, align="C")
    pdf.ln(8)

    # Vertical Line separator
    top_y = pdf.get_y()
    bottom_y = pdf.h - pdf.b_margin
    pdf.set_draw_color(200, 200, 200)
    pdf.set_line_width(0.4)
    pdf.line(pdf.l_margin + epw / 2, top_y, pdf.l_margin + epw / 2, bottom_y)

    # Sections data
    left_sections = [
        ("About Me", context.get("about_me", ""), False),
        ("Skills", context.get("skills", "").split("\n"), True),
        ("Education", context.get("education", "").split("\n"), True),
        ("Projects", context.get("projects", []), True),
    ]

    right_sections = [
        ("Experience", context.get("experience", "").split("\n"), True),
        ("Interests", context.get("interests", "").split("\n"), True),
        ("Social Links", [
            f"{p.capitalize()}: {context.get(p)}"
            for p in ["linkedin", "github", "twitter"] if context.get(p)
        ], True),
    ]

    x_left = pdf.l_margin
    x_right = pdf.l_margin + epw / 2 + 5

    y_start = pdf.get_y()

    # Function to draw header and content, returns height used
    def draw_section_estimate_height(title, content, is_list):
        # header height approx 9 + 2 for line + 5 padding = 16
        base_height = 16
        pdf.set_font('DejaVu', '', 11)
        if is_list and isinstance(content, list):
            total_text = "\n".join([f"• {clean_text(i)}" for i in content])
        else:
            total_text = clean_text(content)
        text_height = pdf.multi_cell_height(col_width, 6, total_text)
        return base_height + text_height

    def draw_section(x, y, title, content, is_list):
        pdf.set_xy(x, y)
        pdf.set_font('DejaVu', '', 15)
        pdf.set_text_color(0, 0, 100)
        pdf.cell(col_width, 9, f"{title}", ln=True)
        pdf.set_draw_color(220, 220, 220)
        pdf.set_line_width(0.4)
        pdf.line(x, pdf.get_y(), x + col_width, pdf.get_y())
        pdf.ln(2)

        pdf.set_font('DejaVu', '', 11)
        pdf.set_text_color(40, 40, 40)

        if is_list and isinstance(content, list):
            for item in content:
                pdf.set_x(x)
                pdf.multi_cell(col_width, 6, f"• {clean_text(item)}", border=0)
        else:
            pdf.set_x(x)
            pdf.multi_cell(col_width, 6, clean_text(content), border=0)

        return pdf.get_y() + 5

    # Calculate total height of left and right sections separately
    left_height = 0
    for title, content, is_list in left_sections:
        left_height += draw_section_estimate_height(title, content, is_list)

    right_height = 0
    for title, content, is_list in right_sections:
        right_height += draw_section_estimate_height(title, content, is_list)

    max_height = max(left_height, right_height)

    # Check if max_height fits in the current page height available
    current_y = pdf.get_y()
    available_height = page_height - (current_y - pdf.t_margin)

    # If doesn't fit, add page break before drawing columns
    if max_height > available_height:
        pdf.add_page()

    # Draw left column
    y_left = pdf.get_y()
    for title, content, is_list in left_sections:
        y_left = draw_section(x_left, y_left, title, content, is_list)

    # Draw right column
    y_right = pdf.get_y()
    # Start right column at same y as left column start (important)
    y_right = pdf.get_y() - left_height + (y_left - pdf.get_y())  # Align top lines of left and right col

    # To ensure right column always starts at the top of left column:
    y_right = pdf.get_y() - (y_left - pdf.get_y())

    # But simpler is:
    y_right = pdf.get_y() - left_height + left_height - max_height  # Actually this needs care, so:
    y_right = pdf.get_y() - max_height  # Start right at the same top as left

    y_right = pdf.get_y() - max_height
    # Actually better to reset to the y after page break or new page, so let's set y_right to same as y_left start
    y_right = pdf.get_y() if max_height <= available_height else pdf.t_margin + 10

    # So final better approach:
    y_right = pdf.get_y() if max_height <= available_height else pdf.t_margin + 10

    # Draw right sections normally (side by side)
    y_right = pdf.get_y() if max_height <= available_height else pdf.t_margin + 10
    for title, content, is_list in right_sections:
        y_right = draw_section(x_right, y_right, title, content, is_list)

    pdf_output = pdf.output(dest='S').encode('latin1', 'ignore')
    return BytesIO(pdf_output)






def get_pdf_download_link(pdf_file):
    with open(pdf_file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    href = f'<a href="data:application/pdf;base64,{base64_pdf}" download="{pdf_file}">📥 Download Your Styled CV as PDF</a>'
    return href




USERS_FILE = "data/users.csv"
PAYMENTS_FILE = "data/payments.csv"
PREMIUM_USERS_FILE = "data/premium_userss.csv"
os.makedirs("data", exist_ok=True)
for file, columns in [
    (USERS_FILE, ["email", "password"]),
    (PAYMENTS_FILE, ["email", "phone", "account_name", "screenshot_name"]),
    (PREMIUM_USERS_FILE, ["email", "status"])
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
        0% {opacity: 0; transform: scale(0.95) translateY(-20px);}
        100% {opacity: 1; transform: scale(1) translateY(0);}
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
            from {opacity: 0; transform: translateY(-30px);}
            to {opacity: 1; transform: translateY(0);}
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
        st.markdown(
            "<b>Enjoy! You now have access to AI CV Generator under Premium Tools tab</b>", 
            unsafe_allow_html=True
        )
    else:
        st.warning("🔓 Free User")
    
    st.markdown("---")
    
    if st.button("🚪 Logout"):
        for key in list(st.session_state.keys()):
            st.session_state[key] = False
        st.rerun()





# ---------- CHECK PREMIUM ----------
premium_users_df = pd.read_csv(PREMIUM_USERS_FILE)
user_row = premium_users_df[premium_users_df["email"] == st.session_state.current_user]
if not user_row.empty:
    status_value = user_row.iloc[0]["status"]
    if isinstance(status_value, str) and status_value.strip().lower() == "verified":
        st.session_state.is_premium = True
    else:
        st.session_state.is_premium = False
else:
    st.session_state.is_premium = False

# ---------- MAIN TABS ----------
tabs = [
    "📘 Resume Preview",
    "📊 Score & Summary",
    "✅ Experience",
    "💡 Suggestions",
    "📌 Skills & Analysis",
    "💎 Premium Features"
]
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
                <div style="padding: 20px; background-color: #f8f9fa; border-radius: 10px; border: 1px solid #ddd;">
                <h3 style="color:#2c3e50;">🚀 Unlock Premium Tools & Boost Your Career!</h3>
                <p style="font-size:16px; color:#34495e;">
                    Get access to exclusive features including:
                </p>
                <ul style="color:#2c3e50; font-size:15px;">
                    <li>🤖 AI-Powered CV Builder</li>
                    <li>📊 Job Match Analyzer</li>
                    <li>🔍 Recruiter Scan Insights</li>
                    <li>📄 Downloadable PDF Templates</li>
                </ul>
                <p style="font-size:16px; color:#27ae60;"><strong>One-Time Access Fee:</strong> <span style="color:#d35400; font-weight:bold;">RS.900 or (3$)</span></p>
                <p style="font-size:15px; color:#34495e;">
                    <strong>💳 Available Payment Methods:</strong><br>
                    ✅ Easypaisa<br>
                    ✅ JazzCash<br>
                    ✅ Stripe (Credit/Debit Card)<br>
                </p>
                <div style="border: 2px dashed #ccc; padding: 15px; border-radius: 10px; background-color: #ffffff; margin-top: 10px;">
                    <strong>📱 Easypaisa / JazzCash:</strong> 0323-2204085 (Muhammad Noaman Saud)
                </div>
                <p style="font-size:14px; color:#7f8c8d; margin-top:10px;">* After payment, submit your details below. Admin will verify your access shortly.</p>
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
                        st.success("✅ Payment details submitted. Admin will verify shortly.")
                    else:
                        st.error("❗ Please fill all fields and upload screenshot.")
                    
                st.markdown("---")  # horizontal line separator

                st.subheader("💳 Stripe Payment")
                st.markdown("### Pay with Stripe (3$)")
                st.info("Pay with Stripe to unlock Premium Tools.")

                # User fills basic info
                stripe_account_name = st.text_input("Account Holder Name", key="account_stripe")
                stripe_phone = st.text_input("Phone Number (Optional)", key="phone_stripe")


                st.markdown("👉 Click below to pay securely:")
                st.markdown("""
                <a href="https://buy.stripe.com/test_8x228tbnRdV86Vrc490VO00" target="_blank">
                            <br>
                    <button style='padding: 10px 20px; font-size: 16px; background-color: #2E86C1; color: white; border-radius: 5px;'>Pay via Stripe</button>
                            </br>
                </a>
                """, unsafe_allow_html=True)
                
                st.warning("After payment, come back and click Confirm Payment.")
                st.markdown("---")  # horizontal line separator

                if st.button("✅ Confirm Payment"):
                    if not stripe_account_name:
                        st.error("❗ Please enter Account Holder Name before confirming payment.")
                    else:
                        try:
                            payments_df = pd.read_csv(PAYMENTS_FILE)
                        except FileNotFoundError:
                            payments_df = pd.DataFrame(columns=["email", "phone", "account_name", "screenshot_name"])

                                            # Check if user already submitted Stripe payment to avoid duplicates
                        existing = payments_df[
                            (payments_df["email"] == st.session_state.current_user) & 
                            (payments_df["screenshot_name"] == "stripe_payment")
                        ]
                        if not existing.empty:
                            st.info("You have already submitted a Stripe payment. Await admin verification.")
                        else:
                    # Append new payment record for Stripe
                            new_payment = {
                                "email": st.session_state.current_user,
                                "phone": stripe_phone,
                                "account_name": stripe_account_name,
                                "screenshot_name": "stripe_payment",  # special flag for Stripe payments
                            }
                            payments_df = pd.concat([payments_df, pd.DataFrame([new_payment])], ignore_index=True)
                            payments_df.to_csv(PAYMENTS_FILE, index=False)
                            st.success("✅ Stripe payment confirmed. Admin will verify shortly.")

 


                st.success("✅ Stripe payment submitted! Please wait for admin verification.")


                # stripe_url = "https://buy.stripe.com/test_8x228tbnRdV86Vrc490VO00"
                # st.markdown(f"""
                #     <a href="{stripe_url}" target="_blank">
                #         <button style="background-color:#4CAF50; color:white; padding:10px 20px;
                #                        border:none; border-radius:5px; cursor:pointer;">
                #             Pay $3 via Stripe
                #         </button>
                #     </a>
                # """, unsafe_allow_html=True)



        if st.session_state.is_premium and len(tab_objs) > 6:
            with tab_objs[6]:
                st.subheader("🌟 Premium Tools")
                st.markdown("""
                💼 Elevate Your Career with Premium Tools
                            
                Welcome to the **Premium Zone** of Smart Resume Analyzer – where your job search transforms from ordinary to outstanding.
                            
                🎁 What’s Included Today:

                - 🧠 **AI-Powered CV Generator**  
                Create a professional, tailored CV in seconds – crafted by advanced AI to match your field.

                - 📄 **Instant PDF Download**  
                 Get beautifully formatted, job-ready resumes that you can download and share instantly.
                
                🚧 Coming Soon – Built Just for You:

                - 🔍 **Smart Job Match Finder**  
                 Discover job openings that perfectly align with your skills, experience, and interests.

                - 📊 **ATS Optimization Analyzer**  
                 Learn how your CV performs in real-world hiring systems and improve your chances.

                - 🕵️‍♂️ **Recruiter View Simulator**  
                 See your resume through the eyes of recruiters and fix what they might skip.

                - 💡 **Real-time AI Suggestions**  
                 Receive smart, personalized tips to boost every section of your resume.
                            
                🌟 Why Go Premium?

                You’re not just making a resume — you’re making a **first impression**. These tools help you stand out, get noticed, and land interviews faster.

                🔔 *This is just the beginning. More smart tools are on the way – stay ahead of the game!*
                """, unsafe_allow_html=True)

                st.title("🧠 **AI-Powered CV Generator")

                st.subheader("✍️ Fill the form to generate your CV")
                name = st.text_input("Full Name")
                education = st.text_area("Education")
                email = st.text_input("Email")
                experience = st.text_area("Work Experience")
                about_me = st.text_area("About_Me")
                skills = st.text_area("Skills")
                interests = st.text_area("Interests")
                projects = st.text_area("Projects Links")
                linkedin = st.text_input("LinkedIn URL")
                github = st.text_input("GitHub URL")
                twitter = st.text_input("Twitter URL (Optional)")
                profile_pic = st.file_uploader("Upload Profile Image (Optional)", type=["png", "jpg", "jpeg"])

                
                if st.button("🚀 Generate CV as PDF"):
                    if not name or not email or not about_me:
                        st.warning("Please fill at least name, email, and about me section.")
                    else:
                        profile_image_url = "https://bootdey.com/img/Content/avatar/avatar7.png"
                        if profile_pic:
                            img_bytes = profile_pic.read()
                            profile_image_url = f"data:image/png;base64,{base64.b64encode(img_bytes).decode()}"

                        context = {
                            "name": name,
                            "email": email,
                            "education": education,
                            "experience": experience,
                            "about_me": about_me,
                            "interests": interests,
                            "skills": skills,
                            "projects": projects.split("\n"),
                            "linkedin": linkedin,
                            "github": github,
                            "twitter": twitter,
                            "profile_image_url": profile_image_url
                        }

                        filename = f"{name.replace(' ', '_')}_cv.pdf"
                        pdf_file = render_pdf_from_data(context)  # This returns BytesIO stream

                        if pdf_file:
                            st.success("✅ CV generated successfully!")
                            st.download_button(
                                label="Download Your CV as PDF",
                                data=pdf_file,
                                file_name=filename,
                                mime="application/pdf"
                            )
                        else:
                            st.error("❌ Failed to generate CV. Please check inputs.")
                st.info("You're already verified for premium access. Enjoy these tools and stay tuned for updates!")
