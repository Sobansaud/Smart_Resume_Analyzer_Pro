import streamlit as st
import pandas as pd
import os

# File paths
PAYMENTS_FILE = "data/payments.csv"
PREMIUM_USERS_FILE = "data/premium_userss.csv"

# Admin credentials
ADMIN_EMAIL = "sobansaud3@gmail.com"
ADMIN_PASS = "soban123"

st.set_page_config(page_title="🔐 Admin Dashboard", layout="centered")
st.title("📊 Admin Payment Dashboard")

# Login section
email = st.text_input("Admin Email")
password = st.text_input("Password", type="password")

# Helper to load users
def load_premium_users():
    if os.path.exists(PREMIUM_USERS_FILE):
        return pd.read_csv(PREMIUM_USERS_FILE)
    else:
        return pd.DataFrame(columns=["email", "status"])

# Helper to save users
def save_premium_users(df):
    df.to_csv(PREMIUM_USERS_FILE, index=False)

if email == ADMIN_EMAIL and password == ADMIN_PASS:
    st.success("🔓 Logged in as Admin")

    if os.path.exists(PAYMENTS_FILE):
        payments_df = pd.read_csv(PAYMENTS_FILE)
        st.subheader("📥 Pending Payments")
        st.dataframe(payments_df)

        verified_email = st.text_input("✍️ Enter email to process")
        col1, col2 = st.columns(2)

        if col1.button("✅ Verify"):
            if verified_email:
                current_df = load_premium_users()
                if verified_email not in current_df["email"].values:
                    new_row = pd.DataFrame([[verified_email, "verified"]], columns=["email", "status"])
                    updated = pd.concat([current_df, new_row], ignore_index=True)
                else:
                    current_df.loc[current_df["email"] == verified_email, "status"] = "verified"
                    updated = current_df
                save_premium_users(updated)
                st.success(f"🎉 {verified_email} marked as premium (verified).")
            else:
                st.error("Please enter an email.")

        if col2.button("❌ Decline"):
            if verified_email:
                current_df = load_premium_users()
                if verified_email not in current_df["email"].values:
                    new_row = pd.DataFrame([[verified_email, "declined"]], columns=["email", "status"])
                    updated = pd.concat([current_df, new_row], ignore_index=True)
                else:
                    current_df.loc[current_df["email"] == verified_email, "status"] = "declined"
                    updated = current_df
                save_premium_users(updated)
                st.warning(f"🚫 {verified_email} marked as declined.")
            else:
                st.error("Please enter an email.")
    else:
        st.info("No payment data found yet.")

    # Show all processed users
    st.subheader("📋 All Processed Users")
    all_users = load_premium_users()
    for i, row in all_users.iterrows():
        user_email = row["email"]
        status = str(row.get("status", "")).strip().lower()
        icon = "✔️" if status == "verified" else "❌"
        color = "green" if status == "verified" else "red"
        display_status = status.capitalize()

        st.markdown(
            f"<div style='border:1px solid {color}; padding:10px; border-radius:5px; margin:5px 0;'>"
            f"<b>{user_email}</b> — <span style='color:{color}; font-weight:bold'>{icon} {display_status}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
else:
    st.warning("Please login as admin to continue.")
