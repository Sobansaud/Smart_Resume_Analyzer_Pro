Smart Resume Analyzer – Professional Resume Analyzer 
Developed by: Muhammad Soban Saud  


Streamlit Link :- []
Dashboard Link :- []

Smart Resume Analyzer is a powerful, AI-driven web application that helps job seekers improve their resumes with data-backed suggestions, real-time skill analysis, and premium tools. Developed as part of a $10 Web App Challenge, this project demonstrates a complete system built with Python (OOP), Streamlit,Authentication  and manual payment integration (Easypaisa & JazzCash), offering both free and premium career tools.


(Key Highlights):-

AI-powered resume parsing and scoring.

Instant skill extraction & personalized suggestions.

Manual payment verification system with lifetime premium access.

Admin dashboard for managing users and payment verification.



What Does Smart Resume Analyzer Offer?
-----------------------
(Free Features)

Upload your resume (PDF format)

Automatically extract skills and keywords

Resume optimization score out of 100

Visual skill frequency chart & word cloud

Suggestions to improve experience and projects
-----------------------

Premium Features (Rs. 300 One-Time Payment)

Currently, once verified, you’ll receive a professionally written AI-generated CV directly to your email address.

(Coming Soon for Premium Users):

- Downloadable resume feedback PDF with expert formatting
- Smart job match insights (powered by mock data or AI)
- Lifetime access to future premium updates

--------------------------

(Authentication System)
Admin Login Email :- sobansaud3@gmail.com
Admin Login Password :- soban123

- Sign up and sign in using email and password
- Credentials stored securely in `data/users.csv`
- Session state used to manage active login
- Premium access is verified using `premium_userss.csv

-------------------------

Payment Process (Manual)

- One-time payment of Rs. 300 via Easypaisa or JazzCash
- User submits:
  • Phone number  
  • Account holder name  
  • Screenshot of the transaction  
- Details stored in `data/payments.csv`
- Admin verifies manually through admin dashboard
- Verified emails are added to `premium_userss.csv`
- Premium features are unlocked automatically on next login

Payment Details:
Easypaisa/JazzCash: 0323-2204085  
Amount: Rs. 300

------------------------



Admin Dashboard Workflow

- Admin launches the dashboard (`admin_dashboard.py`)
- Sees submitted payment requests from users
- Verifies each payment manually by clicking "Verify"
- Upon verification, the user’s email is saved to `premium_userss.csv`
- User gains access to Premium Tools instantly on app refresh

Admin Tools:
- View all pending payment requests
- Mark users as verified with a button click
- System automatically updates access based on `premium_userss.csv`

---

(Files Used)

- `users.csv`: Stores user credentials
- `payments.csv`: Stores submitted payment info
- `premium_userss.csv`: Tracks verified premium users
- `skills.csv`: Contains the dataset of recognized skills

---

(Technology Stack)

- Python (OOP): Classes for resume reading, scoring, and suggestions
- Streamlit: Web app interface
- FPDF: PDF report generation
- Plotly & WordCloud: Visualization tools
- Pandas: Data management and filtering
- Google Generative AI (Gemini): For generating AI-based CVs(coming soon)

---

---

(How It Works – Step-by-Step)

1. User lands on the app, sees the animated logo screen
2. Signs up or logs in using email and password
3. Uploads resume (PDF only)
4. Resume text is extracted using the ResumeReader class
5. Skills are identified and compared with the skills dataset
6. Resume score is calculated with scoring logic
7. Word cloud and frequency charts are generated
8. Suggestions are shown for improving resume
9. If user pays and is verified:
   - Unlocks Premium Tools tab
   - Can Receive AI CVs, download feedback PDFs, and more tools are coming soon 

---

(Why This Project Stands Out):-

- Clean design with animated branding screen
- Built entirely with Object-Oriented Programming
- Manual yet secure payment integration (without Stripe or DB)
- Offers real-world AI-enhanced resume feedback
- Simple admin panel for verifying payments
- All data handled through lightweight CSVs

---

(Assignment Context)

This project was created as part of a $10 assignment challenge:
- Python backend with OOP design
- Streamlit as frontend
- Manual payment system using Easypaisa/JazzCash
- Target: Build a useful, real-world freelancing-ready product

---



