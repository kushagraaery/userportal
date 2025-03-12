import streamlit as st
import pandas as pd
import base64
import requests
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO
import os
from datetime import datetime

# GitHub Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Add your GitHub token in the .env file
GITHUB_REPO = "kushagraaery/adminportal"  # Replace with your GitHub repo
BRANCH = "main"  # Change if needed
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/"

def upload_file_to_github(file, file_label):
    if file:
        file_name = file.name
        file_content = file.getvalue()
        encoded_content = base64.b64encode(file_content).decode()
        
        # Check if file exists in the repository
        response = requests.get(f"{GITHUB_API_URL}{file_name}", headers={"Authorization": f"token {GITHUB_TOKEN}"})
        sha = response.json().get("sha", "") if response.status_code == 200 else None
        
        # Prepare payload
        payload = {
            "message": f"Upload {file_name} via Streamlit",
            "content": encoded_content,
            "branch": BRANCH,
        }
        if sha:
            payload["sha"] = sha  # Include SHA to update existing file
        
        # Upload file to GitHub
        upload_response = requests.put(f"{GITHUB_API_URL}{file_name}", json=payload, headers={"Authorization": f"token {GITHUB_TOKEN}"})
        
        if upload_response.status_code in [200, 201]:
            st.sidebar.success(f"{file_label} file '{file_name}' successfully uploaded to Incedo Database!")
        else:
            st.sidebar.error(f"Failed to upload {file_label} file: {upload_response.json()}")

# GitHub Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Add your GitHub token in the .env file
GITHUB_REPO = "kushagraaery/adminportal"  # Replace with your GitHub repo
FILE_NAME = "Generated_Responses.xlsx"
BASE_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_NAME}"

 # Helper function to fetch Excel file from GitHub
def fetch_excel_from_github():
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.get(BASE_URL, headers=headers)
    if response.status_code == 200:
        content = response.json()
        file_data = base64.b64decode(content["content"])
        df = pd.read_excel(BytesIO(file_data))
        sha = content["sha"]  # Required for updating the file
        return df, sha
    else:
        st.error("Failed to fetch the Excel file from GitHub.")
        return None, None

# Streamlit UI
st.title("User Portal")

st.markdown('<div class="content-section">', unsafe_allow_html=True)
st.subheader("What is a Society?")
st.write(
    "An **ES Society** is an organization within a state that may or may not ladder to a national society "
    "(e.g., FLASCO to ASCO).\n\n"
    "- Member supported\n"
    "- Board or governing body may encompass key state TAEs\n"
    "- Partnerships include state agencies: Advocacy, Policy, Payor, etc.\n"
    "- Defined state-influenced engagement strategy: education, data dissemination, support of state oncology HCPs, "
    "creation of resources to increase access to care on the state level."
)
st.markdown('</div>', unsafe_allow_html=True)

time.sleep(0.5)

st.markdown('<div class="content-section">', unsafe_allow_html=True)
st.subheader("Difference Between Society & Conference")
st.write(
    "- An **ES Society** may include annual or biannual conferences to engage the broader public, members, and HCPs.\n"
    "- Not all ES conferences align with state societies (e.g., Moffitt, Great Debates, UAB Review).\n"
    "- A **Conference** may align with an academic center or health system."
)
st.markdown('</div>', unsafe_allow_html=True)

time.sleep(0.5)

st.markdown('<div class="content-section">', unsafe_allow_html=True)
st.subheader("Tiering System for Society Engagement")
st.write(
    "When identifying a society to engage, apply the **ES Society Attributes** to each society. Societies are then tiered as follows:\n"
    "- **Tier 0 (High Priority):** Society meets most attributes (>5) and provides strong opportunities for implementing the medical strategic framework.\n"
    "- **Tier 1 (Medium Priority):** Society meets 3-5 attributes but may not allow full implementation of the Society Framework. Future engagement can be explored.\n"
    "- **Tier 2 (Low Priority):** Society does not meet attributes in full and does not warrant immediate investment. Re-evaluation may be needed in the future."
)
st.markdown('</div>', unsafe_allow_html=True)

st.sidebar.header("Upload Files")

# File uploaders in sidebar
society_file = st.sidebar.file_uploader("Upload Society Names (CSV/Excel)", type=["csv", "xlsx"], key="society")
questions_file = st.sidebar.file_uploader("Upload Questions (CSV/Excel)", type=["csv", "xlsx"], key="questions")

submit_button = st.sidebar.button("Submit Data")

if submit_button:
    if not society_file and not questions_file:
        st.sidebar.warning("Please upload at least one file before submitting.")
    else:
        if society_file:
            upload_file_to_github(society_file, "Society Names")
        if questions_file:
            upload_file_to_github(questions_file, "Questions")
        with st.spinner("Wait for a few seconds for the data to update..."):
                time.sleep(10)
                st.page_link("http://localhost:8501/", label="Navigate to Admin Portal", icon="📝")

    def send_email(smtp_server, smtp_port, sender_email, sender_password, receiver_email, subject, html_content):
        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(html_content, "html"))
    
        # Choose whether to use SSL or TLS
        try:
            if smtp_port == 465:  # Use SSL
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    server.login(sender_email, sender_password)
                    server.send_message(msg)
            elif smtp_port == 587:  # Use TLS
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()  # Secure the connection
                    server.login(sender_email, sender_password)
                    server.send_message(msg)
            return "Email sent successfully!"
        except Exception as e:
            return f"Failed to send email: {e}"
        
    # Collect email details from user input
    receiver_email = "kushagra.sharma1@incedoinc.com"
    email_subject = "Data Updation in Incedo Database"
    
    # Set Gmail SMTP server settings
    smtp_server = "smtp.gmail.com"  # Gmail SMTP server
    smtp_port = 587  # Choose SSL or TLS
    
    # Set your sender email here (e.g., your Gmail)
    sender_email = "johnwickcrayons@gmail.com"
    sender_password = "afpt eoyt asaq qzjh"
    
    # Send email if button clicked
    if receiver_email and email_subject and sender_email and sender_password:
        email_body = f"""
        <html>
        <head>
        </head>
        <body>
            <p>Dear Recipient,</p>
            <p>New data is uploaded to the Incedo Database!</p>
            <p>Best regards,<br>Incedo Admin Team</p>
        </body>
        </html>
        """
        status = send_email(smtp_server, smtp_port, sender_email, sender_password, receiver_email, email_subject, email_body)
        # Display success or error message
        if "successfully" in status:
            st.success("Successfully sent updation mail to Incedo Admin Team! Please wait for a week for the Incedo Admin Team to review the prompts and fetch you the data")
        else:
            st.error("Error while sending updation mail to Incedo Admin Team!")

if st.button("View Historic Data"):
    df, sha = fetch_excel_from_github()
    if df is not None:
        last_updated = df.iloc[0]["Last Updated"]
        last_updated_dt = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")
        formatted_date = last_updated_dt.strftime("%d %B %Y")
        st.success(f"Current Data Last updated on: {formatted_date}")
        st.write("Current Data:")
        st.dataframe(df)
