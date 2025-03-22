import pandas as pd
import pdfplumber
import os

def extract_data(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()  # Get file extension

    if file_extension == ".csv":
        return extract_from_csv(file_path)
    elif file_extension == ".pdf":
        return extract_from_pdf(file_path)
    else:
        raise ValueError(f"❌ Unsupported file format ({file_extension}). Use CSV or PDF.")

def extract_from_csv(file_path):
    df = pd.read_csv(file_path)
    required_columns = {"first_name", "last_name", "email", "phone", "address"}
    
    if not required_columns.issubset(df.columns):
        raise ValueError("❌ CSV file must contain 'first_name', 'last_name', 'email', 'phone', and 'address' columns.")
    
    return df.to_dict(orient="records")

def extract_from_pdf(file_path):
    users = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                for line in text.split("\n"):
                    parts = line.split(",")  # Adjust if your PDF format differs
                    if len(parts) == 5:
                        users.append({
                            "first_name": parts[0].strip(),
                            "last_name": parts[1].strip(),
                            "email": parts[2].strip(),
                            "phone": parts[3].strip(),
                            "address": parts[4].strip(),
                        })
    if not users:
        raise ValueError("❌ No valid data extracted from the PDF.")
    
    return users
