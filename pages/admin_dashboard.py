import streamlit as st
import pandas as pd
import os

PAYMENTS_FILE = "data/payments.csv"
PREMIUM_USERS_FILE = "data/premium_userss.csv"

ADMIN_EMAIL = "sobansaud3@gmail.com"
ADMIN_PASS = "soban123"

st.set_page_config(page_title="🔐 Admin Dashboard", layout="centered")
st.title("📊 Admin Payment Dashboard")

email = st.text_input("Admin Email")
password = st.text_input("Password", type="password")

if email == ADMIN_EMAIL and password == ADMIN_PASS:
    st.success("🔓 Logged in as Admin")

    if os.path.exists(PAYMENTS_FILE):
        payments_df = pd.read_csv(PAYMENTS_FILE)
        st.subheader("📥 Pending Payments")
        st.dataframe(payments_df)

        verified_email = st.text_input("✍️ Enter email to verify as premium")
        if st.button("✅ Verify"):
            if verified_email:
                if os.path.exists(PREMIUM_USERS_FILE):
                    current = pd.read_csv(PREMIUM_USERS_FILE)
                else:
                    current = pd.DataFrame(columns=["email"])
                if verified_email not in current["email"].values:
                    updated = pd.concat([current, pd.DataFrame([[verified_email]], columns=["email"])], ignore_index=True)
                    updated.to_csv(PREMIUM_USERS_FILE, index=False)
                    st.success(f"🎉 {verified_email} marked as premium user.")
                else:
                    st.info("Already verified.")
            else:
                st.error("Please enter an email.")
    else:
        st.info("No payment data found yet.")
