import streamlit as st
import pandas as pd
import os

PAYMENTS_FILE = "data/payments.csv"
PREMIUM_USERS_FILE = "data/premium_userss.csv"

ADMIN_EMAIL = "sobansaud3@gmail.com"
ADMIN_PASS = "soban123"

st.set_page_config(page_title="🔐 Admin Dashboard", layout="centered")
st.title("📊 Admin Payment Dashboard")

# --- Admin Login ---
email = st.text_input("Admin Email")
password = st.text_input("Password", type="password")

if email == ADMIN_EMAIL and password == ADMIN_PASS:
    st.success("🔓 Logged in as Admin")

    # --- Load data only after successful login ---
    if not os.path.exists(PAYMENTS_FILE):
        st.warning("No payments yet.")
        st.stop()

    payments_df = pd.read_csv(PAYMENTS_FILE)

    if os.path.exists(PREMIUM_USERS_FILE) and os.path.getsize(PREMIUM_USERS_FILE) > 0:
        premium_df = pd.read_csv(PREMIUM_USERS_FILE)
    else:
        premium_df = pd.DataFrame(columns=["email"])

    verified_emails = premium_df["email"].tolist()
    unverified_payments = payments_df[~payments_df["email"].isin(verified_emails)]

    st.subheader("🧾 Pending Payment Verifications")

    if unverified_payments.empty:
        st.info("No pending verifications.")
    else:
        for index, row in unverified_payments.iterrows():
            st.markdown(f"""
            **Email**: {row['email']}  
            **Phone**: {row['phone']}  
            **Account Name**: {row['account_name']}  
            **Screenshot**: {row['screenshot_name']}  
            """)
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"✅ Verify {row['email']}", key=f"verify_{index}"):
                    new_row = pd.DataFrame([[row["email"]]], columns=["email"])
                    new_row.to_csv(PREMIUM_USERS_FILE, mode='a', header=False, index=False)
                    st.success(f"{row['email']} verified as premium user.")
                    st.rerun()

            with col2:
                if st.button(f"❌ Decline {row['email']}", key=f"decline_{index}"):
                    payments_df.drop(index, inplace=True)
                    payments_df.to_csv(PAYMENTS_FILE, index=False)
                    st.warning(f"{row['email']} payment declined and removed.")
                    st.rerun()
else:
    st.info("🔒 Please enter valid admin credentials to view the dashboard.")

