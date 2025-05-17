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

# class CustomPDF(FPDF):
#     def __init__(self):
#         super().__init__(format=(210, 360))  # increased height
#         self.set_auto_page_break(False)

# def render_pdf_from_data(context):
#     pdf = CustomPDF()
#     pdf.add_page()

#     epw = pdf.w - 2 * pdf.l_margin
#     col_width = epw / 2 - 5
#     margin_top = 10

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
#                 pdf.image(tmpfile.name, x=pdf.w / 2 - 20, y=margin_top, w=40, h=40)
#                 os.unlink(tmpfile.name)
#         except:
#             pass
#     pdf.set_y(margin_top + 45)

#     # === Name and Email ===
#     pdf.set_font('DejaVu', '', 20)
#     pdf.cell(0, 10, clean_text(context.get("name", "John Doe")), ln=True, align="C")
#     pdf.set_font('DejaVu', '', 12)
#     pdf.cell(0, 8, f"Email: {clean_text(context.get('email', 'johndoe@example.com'))}", ln=True, align="C")
#     pdf.ln(6)

#     # Draw separation line full page height:
#     top_y = pdf.get_y()
#     bottom_y = pdf.h - pdf.b_margin
#     pdf.set_draw_color(180, 180, 180)
#     pdf.set_line_width(0.3)
#     pdf.line(pdf.l_margin + epw / 2, top_y, pdf.l_margin + epw / 2, bottom_y)

#     # Sections
#     left_sections = [
#         ("About Me", context.get("about_me", ""), False),
#         ("Education", context.get("education", "").split("\n"), True),
#         ("Interests", context.get("interests", "").split("\n"), True),
#         ("Social Links", [
#             f"{p.capitalize()}: {context.get(p)}"
#             for p in ["linkedin", "github", "twitter"] if context.get(p)
#         ], True),
#     ]

#     right_sections = [
#         ("Experience", context.get("experience", "").split("\n"), True),
#         ("Projects", context.get("projects", []), True),
#         ("Skills", context.get("skills", "").split("\n"), True),
#     ]

#     x_left = pdf.l_margin
#     x_right = pdf.l_margin + epw / 2 + 5

#     y_left = pdf.get_y()
#     y_right = y_left

#     # Function to draw left column fully
#     def draw_section_full(x, y, title, content, is_list):
#         pdf.set_xy(x, y)
#         pdf.set_font('DejaVu', '', 14)
#         pdf.cell(col_width, 8, f"{title}:", ln=True)
#         pdf.set_font('DejaVu', '', 11)
#         pdf.set_x(x)
#         if is_list and isinstance(content, list):
#             for item in content:
#                 pdf.set_x(x)
#                 pdf.multi_cell(col_width, 6, f"• {clean_text(item)}")
#         else:
#             pdf.multi_cell(col_width, 6, clean_text(content))
#         return pdf.get_y() + 2

#     # Draw all left sections fully on page 1
#     for title, content, is_list in left_sections:
#         y_left = draw_section_full(x_left, y_left, title, content, is_list)

#     # For right sections: draw with splitting if needed

#     bottom_y = pdf.h - pdf.b_margin

#     def draw_section_split(x, y, title, content, is_list):
#         """Draw section at (x,y), if content too long split over pages.
#         Return last y on last page."""
#         pdf.set_font('DejaVu', '', 14)
#         line_height = 6

#         def draw_title(y_pos):
#             pdf.set_xy(x, y_pos)
#             pdf.set_font('DejaVu', '', 14)
#             pdf.cell(col_width, 8, f"{title}:", ln=True)
#             pdf.set_font('DejaVu', '', 11)

#         # Draw title
#         if y + 8 > bottom_y:
#             pdf.add_page()
#             # redraw vertical line
#             new_top = pdf.get_y()
#             pdf.set_draw_color(180,180,180)
#             pdf.set_line_width(0.3)
#             pdf.line(pdf.l_margin + epw/2, new_top, pdf.l_margin + epw/2, bottom_y)
#             y = new_top
#         draw_title(y)
#         y += 8

#         if not is_list:
#             # For non-list content, just multiline text
#             text = clean_text(content)
#             # Break text into lines roughly (FPDF multi_cell will do it)
#             pdf.set_xy(x, y)
#             # Check if enough space for all content, else new page
#             estimated_height = line_height * (len(text) // 40 + 1)
#             if y + estimated_height > bottom_y:
#                 # Split text roughly in half
#                 midpoint = len(text)//2
#                 # Try to break on space
#                 split_pos = text.rfind(' ', 0, midpoint)
#                 if split_pos == -1:
#                     split_pos = midpoint
#                 part1 = text[:split_pos]
#                 part2 = text[split_pos:]

#                 pdf.multi_cell(col_width, line_height, part1)
#                 pdf.add_page()
#                 # redraw line
#                 new_top = pdf.get_y()
#                 pdf.set_draw_color(180,180,180)
#                 pdf.set_line_width(0.3)
#                 pdf.line(pdf.l_margin + epw/2, new_top, pdf.l_margin + epw/2, bottom_y)
#                 pdf.set_xy(x, new_top)
#                 pdf.multi_cell(col_width, line_height, part2)
#                 y = pdf.get_y() + 2
#             else:
#                 pdf.multi_cell(col_width, line_height, text)
#                 y = pdf.get_y() + 2
#             return y

#         # If list content, handle line by line with split
#         for i, item in enumerate(content):
#             line = f"• {clean_text(item)}"
#             needed_height = line_height
#             if y + needed_height > bottom_y:
#                 # New page, redraw line
#                 pdf.add_page()
#                 new_top = pdf.get_y()
#                 pdf.set_draw_color(180,180,180)
#                 pdf.set_line_width(0.3)
#                 pdf.line(pdf.l_margin + epw/2, new_top, pdf.l_margin + epw/2, bottom_y)
#                 y = new_top
#                 draw_title(y - 8)  # redraw title slightly above content
#                 y += 8
#             pdf.set_xy(x, y)
#             pdf.multi_cell(col_width, line_height, line)
#             y = pdf.get_y()
#         return y + 2

#     # Draw right sections with splitting
#     for title, content, is_list in right_sections:
#         y_right = draw_section_split(x_right, y_right, title, content, is_list)

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

class CustomPDF(FPDF):
    def __init__(self):
        super().__init__(format=(210, 360))  # increased height
        self.set_auto_page_break(False)

def render_pdf_from_data(context):
    pdf = CustomPDF()
    pdf.add_page()

    epw = pdf.w - 2 * pdf.l_margin
    col_width = epw / 2 - 5
    margin_top = 10

    font_path = os.path.join(os.path.dirname(__file__), 'DejaVuSans.ttf')
    if not os.path.isfile(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")
    pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.add_font('DejaVu', 'B', font_path, uni=True)  # bold version
    pdf.set_font('DejaVu', '', 12)

    # === Image ===
    image_url = context.get("profile_image_url", "")
    if image_url.startswith("data:image"):
        try:
            header, encoded = image_url.split(",", 1)
            img_bytes = base64.b64decode(encoded)
            img = Image.open(BytesIO(img_bytes))
            with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                img.save(tmpfile.name)
                pdf.image(tmpfile.name, x=pdf.w / 2 - 20, y=margin_top, w=40, h=40)
                os.unlink(tmpfile.name)
        except:
            pass
    pdf.set_y(margin_top + 45)

    # === Name and Email ===
    pdf.set_font('DejaVu', '', 20)
    pdf.cell(0, 10, clean_text(context.get("name", "John Doe")), ln=True, align="C")
    pdf.set_font('DejaVu', '', 12)
    pdf.cell(0, 8, f"Email: {clean_text(context.get('email', 'johndoe@example.com'))}", ln=True, align="C")
    pdf.ln(6)

    # Draw separation line full page height:
    top_y = pdf.get_y()
    bottom_y = pdf.h - pdf.b_margin
    pdf.set_draw_color(180, 180, 180)
    pdf.set_line_width(0.3)
    pdf.line(pdf.l_margin + epw / 2, top_y, pdf.l_margin + epw / 2, bottom_y)

    left_sections = [
        ("About Me", context.get("about_me", ""), False),
        ("Education", context.get("education", "").split("\n"), True),
        ("Interests", context.get("interests", "").split("\n"), True),
        ("Social Links", [
            f"{p.capitalize()}: {context.get(p)}"
            for p in ["linkedin", "github", "twitter"] if context.get(p)
        ], True),
    ]

    right_sections = [
        ("Experience", context.get("experience", "").split("\n"), True),
        ("Projects", context.get("projects", []), True),
        ("Skills", context.get("skills", "").split("\n"), True),
    ]

    x_left = pdf.l_margin
    x_right = pdf.l_margin + epw / 2 + 5

    y_left = pdf.get_y()
    y_right = y_left

    def draw_section_full(x, y, title, content, is_list):
        pdf.set_xy(x, y)
        pdf.set_font('DejaVu', 'B', 16)  # Bold + larger headers
        pdf.cell(col_width, 8, f"{title}:", ln=True)
        pdf.set_font('DejaVu', '', 11)
        pdf.set_x(x)
        if is_list and isinstance(content, list):
            for item in content:
                pdf.set_x(x)
                pdf.multi_cell(col_width, 6, f"• {clean_text(item)}")
        else:
            pdf.multi_cell(col_width, 6, clean_text(content))
        return pdf.get_y() + 2

    for title, content, is_list in left_sections:
        y_left = draw_section_full(x_left, y_left, title, content, is_list)

    bottom_y = pdf.h - pdf.b_margin

    def draw_section_split(x, y, title, content, is_list):
        pdf.set_font('DejaVu', 'B', 16)
        line_height = 6

        def draw_title(y_pos):
            pdf.set_xy(x, y_pos)
            pdf.set_font('DejaVu', 'B', 16)
            pdf.cell(col_width, 8, f"{title}:", ln=True)
            pdf.set_font('DejaVu', '', 11)

        if y + 8 > bottom_y:
            pdf.add_page()
            new_top = pdf.get_y()
            pdf.set_draw_color(180, 180, 180)
            pdf.set_line_width(0.3)
            pdf.line(pdf.l_margin + epw / 2, new_top, pdf.l_margin + epw / 2, bottom_y)
            y = new_top
        draw_title(y)
        y += 8

        if not is_list:
            text = clean_text(content)
            pdf.set_xy(x, y)
            estimated_height = line_height * (len(text) // 40 + 1)
            if y + estimated_height > bottom_y:
                midpoint = len(text) // 2
                split_pos = text.rfind(' ', 0, midpoint)
                if split_pos == -1:
                    split_pos = midpoint
                part1 = text[:split_pos]
                part2 = text[split_pos:]
                pdf.multi_cell(col_width, line_height, part1)
                pdf.add_page()
                new_top = pdf.get_y()
                pdf.set_draw_color(180, 180, 180)
                pdf.set_line_width(0.3)
                pdf.line(pdf.l_margin + epw / 2, new_top, pdf.l_margin + epw / 2, bottom_y)
                pdf.set_xy(x, new_top)
                pdf.multi_cell(col_width, line_height, part2)
                y = pdf.get_y() + 2
            else:
                pdf.multi_cell(col_width, line_height, text)
                y = pdf.get_y() + 2
            return y

        for i, item in enumerate(content):
            line = f"• {clean_text(item)}"
            needed_height = line_height
            if y + needed_height > bottom_y:
                pdf.add_page()
                new_top = pdf.get_y()
                pdf.set_draw_color(180, 180, 180)
                pdf.set_line_width(0.3)
                pdf.line(pdf.l_margin + epw / 2, new_top, pdf.l_margin + epw / 2, bottom_y)
                y = new_top
                draw_title(y - 8)
                y += 8
            pdf.set_xy(x, y)
            pdf.multi_cell(col_width, line_height, line)
            y = pdf.get_y()
        return y + 2

    for title, content, is_list in right_sections:
        y_right = draw_section_split(x_right, y_right, title, content, is_list)

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
