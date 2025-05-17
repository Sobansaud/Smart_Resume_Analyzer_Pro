
🚀 Smart Resume Analyzer – Professional AI-Powered Resume Builder
===========================================================
Developed by: Muhammad Soban Saud

🔗 Live App: https://smartresumeanalyzerpro-soban.streamlit.app/

🔐 Admin Credentials:
Email: sobansaud3@gmail.com
Password: soban123


🔍 What is Smart Resume Analyzer?
--------------------------------
Smart Resume Analyzer is a cutting-edgeAI-powered web application designed to help job seekers transform their resumes into professional, job-winning documents , Developed as part of a $10 Web App Challenge .  Built entirely using Object-Oriented Programming (OOP) in Python, the app ensures modular, scalable, and efficient functionality across all its features.

This platform combines real-time resume analysis, intelligent keyword extraction, and AI-enhanced suggestions to help users stand out in the job market. With a built-in authentication system and a smooth lifetime premium unlock via both Stripe and manual Easypaisa/JazzCash payments, Smart Resume Analyzer delivers a seamless experience for users globally.

Whether you're a student, a fresh graduate, or a professional looking to upgrade your CV, Smart Resume Analyzer provides both free and premium tools, including:

Real-time skill matching

Personalized suggestions

Beautiful AI-generated CVs

Resume scoring and insights

Secure user login & session management

Admin-verified premium unlock system

All of this is delivered through a modern UI built in Streamlit, with backend logic powered by cleanly structured OOP classes

--------------------------------

(✨ Key Highlights)
✅ AI-powered resume parsing and scoring

📊 Real-time skill extraction and keyword frequency charts

🧠 Personalized improvement suggestions

🔒 Secure login system (email/password)

💳 Manual & Stripe payment integration

🛠️ Admin dashboard to manage and verify users

🌟 Premium AI CV Generator – create a beautiful, professional CV in seconds

--------------------------------

(🆓 Free Features)

Upload resume (PDF format)

Extract keywords & skills

Resume score (out of 100)

WordCloud + skill frequency chart

Instant suggestions to improve resume, experience, and projects
--------------------------------

💎 Premium Features (One-Time Rs. 300 / Stripe Payment)

Once verified, you unlock:

✅ AI CV Generator
Get a professionally formatted CV, beautifully written using generative AI, and downloaded in PDF format using HTML/CSS-styled templates.

📄 Downloadable resume feedback PDF

🔍 Smart job match insights (coming soon)

♾️ Lifetime access to all future premium tools

--------------------------------

(🔐 Authentication System)
Sign up/sign in using email + password

Credentials stored securely in data/users.csv

Active sessions handled using Streamlit session_state

Premium access tracked via premium_userss.csv

--------------------------------

💰 Payment Process – Manual & Stripe
🟢 Option 1: Easypaisa / JazzCash (Manual)
Amount: Rs. 900 or 3$ (one-time)

Send screenshot, name & phone after payment

Details stored in payments.csv

Admin verifies manually

Once approved, email is added to premium_userss.csv

Access unlocked on next login
--------------------------------


🟣 Option 2: Stripe Payment (International)
Secure, real-time Stripe payment support added

After Stripe payment, your email is automatically logged

Admin sees it in the dashboard and verifies it

Once verified, you gain access to Premium Tools instantly
--------------------------------


🛠️ Admin Dashboard (admin_dashboard.py)
View pending payments (manual or Stripe)

One-click Verify to approve access

Email is added to premium_userss.csv

User sees "🌟 Premium Tools" tab on app refresh
--------------------------------

🗂️ Important Files Used
File	Description
users.csv	Stores user credentials
payments.csv	Stores manual payment info
premium_userss.csv	Verified premium users
skills.csv	Resume skills database
template.html	Beautiful AI CV layout
main.py	Streamlit main app(auth,stripe,premium tools etc)
admin_dashboard.py	Admin control panel

--------------------------------

🧰 Tech Stack
Python (OOP): Modular, class-based backend logic

Streamlit: Modern frontend and routing

FPDF: Exporting resume feedback as PDFs

HTML/CSS Templates: Stylish CV layouts

Plotly + WordCloud: Data visualizations

Pandas: File and data operations

Cohere AI (Cohere): For generating AI CVs
--------------------------------


🧭 How It Works (Step-by-Step)
User opens the app, greeted by animated welcome screen with logo

Signs up / logs in with email & password

Uploads PDF resume

ResumeReader class extracts text

SkillMatcher compares skills to dataset

Resume is scored, chart & word cloud generated

Suggestions shown to enhance resume

User can pay manually or via Stripe

Admin verifies, and unlocks premium tools

User accesses tools like AI CV Generator, downloads PDF CV
--------------------------------


🌟 Why Smart Resume Analyzer?
✅ Built using clean OOP architecture

🎨 Beautiful UI with animations and logo branding

💸 Works with manual and Stripe payment

🤖 Offers real-world AI-generated resumes

👨‍💻 Lightweight admin dashboard, no database used

💡 All data handled via simple CSVs
-----------------------------------

📝 Challenge Context
Smart Resume Analyzer was built as part of a competitive $10 Web App Assignment Challenge, with the aim of delivering a real-world, freelancing-ready product using minimal resources.

Despite the strict constraints, the project successfully integrates:

✅ Backend in Python using a clean Object-Oriented Programming (OOP) architecture

✅ Streamlit Frontend with modern UI, animated branding, and intuitive user experience

✅ Secure Email-Based Authentication System

User sign-up/login using email and password

Session management with Streamlit's built-in state handling

User data securely stored in lightweight CSVs

✅ Dual Payment Integration

Manual Payment System via Easypaisa & JazzCash

Stripe Support for international users

✅ Admin Dashboard for manual verification and premium access control

✅ AI-Powered Career Tools: Resume parsing, scoring, and a premium AI-generated CV generator

✅ Freelancing-Ready UI/UX with animated splash screen and professional visualizations

This project stands out as a complete, client-ready web solution demonstrating strong command over Python, AI integration, authentication, and both local/international payment handling — all packaged into a polished, real-world tool.
-------------------------------

📌 Developer: Muhammad Soban Saud
📬 Email: sobansaud3@gmail.com