import streamlit as st
import os
import pandas as pd
import tempfile
import zipfile
from generate_emails import execute_tasks  # Import function from CrewAI script

# Set up Streamlit UI
st.set_page_config(page_title="AI Email Generator", layout="wide")

st.title("📩 AI-Powered Personalized Email Generator")
st.write("Upload a CSV or PDF file containing names, emails, and addresses to generate personalized emails.")

# File uploader
uploaded_file = st.file_uploader("Upload CSV or PDF file", type=["csv", "pdf"])

if uploaded_file is not None:
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    # Process the uploaded file
    with st.spinner("Processing file and generating emails..."):
        output_files = execute_tasks(temp_file_path)  # Now returns [(filename, content), ...]

    if not output_files:
        st.error("❌ Failed to process file. Ensure it is a valid CSV or PDF with correct columns.")
    else:
        st.success("✅ Emails have been generated successfully!")

        st.subheader("📩 Generated Emails:")

        # Display generated emails in Streamlit (without saving them)
        for file_name, content in output_files:
            with st.expander(f"📄 {file_name}"):
                st.text(content)

        # Button to save emails into a zip file
        if st.button("📥 Download All Emails as ZIP"):
            output_dir = "output_emails"
            os.makedirs(output_dir, exist_ok=True)

            zip_file_path = os.path.join(output_dir, "generated_emails.zip")

            with zipfile.ZipFile(zip_file_path, "w") as zipf:
                for file_name, content in output_files:
                    email_path = os.path.join(output_dir, file_name)
                    
                    # Save the email only when ZIP download is clicked
                    with open(email_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    
                    zipf.write(email_path, arcname=file_name)
                    
                    # Delete the individual text file after adding it to ZIP
                    os.remove(email_path)

            # Provide ZIP file for download
            with open(zip_file_path, "rb") as f:
                st.download_button("📥 Download ZIP", f, file_name="generated_emails.zip", mime="application/zip")

            # Clean up ZIP file after download
            os.remove(zip_file_path)

