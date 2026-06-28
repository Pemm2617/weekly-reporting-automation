"""
=============================================================================
Automation 1: Weekly Stakeholder Reporting Pipeline
=============================================================================
Author      : Prem Channapattan
Description : Automates the end-to-end process of picking up vendor index
              files from a designated folder, cleaning and delimiting the
              data, saving processed files with index names, and emailing
              them to respective stakeholders on a scheduled basis.

              Wednesday files  →  Processed  →  Emailed on Thursday
              Friday files     →  Processed  →  Emailed on Monday

NOTE: This is a demonstration script using dummy data.
      Actual implementation was built for internal use at Morningstar India.
      All company-specific details, API endpoints, and internal systems
      have been replaced with generic placeholders.
=============================================================================
"""

import os
import pandas as pd
import smtplib
import logging
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# ── Logging Setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    filename="weekly_reporting.log",
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

# ── Configuration ─────────────────────────────────────────────────────────────
# In production these paths point to actual network/local folders
# Here they point to sample folders for demonstration

CONFIG = {
    "wednesday": {
        "input_folder":  "sample_input_files",
        "output_folder": "processed_files/wednesday",
        "file_keywords": ["APAC_TECH_INDEX", "APAC_FINANCE_INDEX"],
        "stakeholders":  ["stakeholder1@example.com", "stakeholder2@example.com"],
        "email_subject": "Wednesday Index Files — Processed Report",
    },
    "friday": {
        "input_folder":  "sample_input_files",
        "output_folder": "processed_files/friday",
        "file_keywords": ["CEEMEA_ENERGY_INDEX", "CEEMEA_CONSUMER_INDEX"],
        "stakeholders":  ["stakeholder3@example.com", "stakeholder4@example.com"],
        "email_subject": "Friday Index Files — Processed Report",
    },
}

SENDER_EMAIL    = "your_email@example.com"
SENDER_PASSWORD = "your_password"          # Use environment variable in production
SMTP_SERVER     = "smtp.gmail.com"
SMTP_PORT       = 587


# ── Step 1: Pick Files from Input Folder ─────────────────────────────────────
def pick_files(input_folder, file_keywords):
    """
    Scans the input folder and picks files matching the index keywords.
    In production this folder is populated by Outlook rules that move
    vendor emails to a designated folder automatically.
    """
    matched_files = []
    all_files = os.listdir(input_folder)

    for keyword in file_keywords:
        for file in all_files:
            if keyword in file and file.endswith(".csv"):
                matched_files.append(os.path.join(input_folder, file))
                logging.info(f"File matched: {file}")

    if not matched_files:
        logging.warning(f"No files found for keywords: {file_keywords}")

    return matched_files


# ── Step 2: Clean and Process the File ───────────────────────────────────────
def clean_and_process(file_path, output_folder):
    """
    Reads the raw vendor file, cleans the data, delimits with comma,
    and saves the processed file with the index name in the output folder.
    """
    os.makedirs(output_folder, exist_ok=True)

    df = pd.read_csv(file_path)

    # --- Cleaning Steps ---
    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Strip whitespace from string columns
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())

    # Drop rows where Security_ID or Weight is missing
    df.dropna(subset=["Security_ID", "Weight"], inplace=True)

    # Round numeric columns to 4 decimal places
    num_cols = df.select_dtypes(include="number").columns
    df[num_cols] = df[num_cols].round(4)

    # Add processing timestamp
    df["Processed_Date"] = datetime.today().strftime("%Y-%m-%d")

    # --- Save with index name ---
    index_name   = os.path.basename(file_path).replace(".csv", "")
    output_path  = os.path.join(output_folder, f"{index_name}_Processed.csv")
    df.to_csv(output_path, index=False)

    logging.info(f"Processed file saved: {output_path}")
    print(f"  Processed: {output_path}")

    return output_path


# ── Step 3: Send Email with Attachments ──────────────────────────────────────
def send_email(stakeholders, subject, processed_files):
    """
    Sends an email to respective stakeholders with the processed files
    attached. In production this uses the internal SMTP server.
    """
    msg              = MIMEMultipart()
    msg["From"]      = SENDER_EMAIL
    msg["To"]        = ", ".join(stakeholders)
    msg["Subject"]   = subject

    body = (
        f"Dear Stakeholder,\n\n"
        f"Please find attached the processed index files for your reference.\n"
        f"These files have been validated and cleaned as per the standard process.\n\n"
        f"Files attached: {len(processed_files)}\n"
        f"Processed on  : {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"This is an automated email. Please do not reply to this message.\n\n"
        f"Regards,\n"
        f"Index Data Operations Team"
    )
    msg.attach(MIMEText(body, "plain"))

    # Attach each processed file
    for file_path in processed_files:
        with open(file_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(file_path)}"
            )
            msg.attach(part)

    # --- Send via SMTP ---
    # NOTE: In production replace with internal SMTP credentials
    # Uncomment below block when running with real email credentials
    """
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, stakeholders, msg.as_string())
    """

    # For demo purposes — simulate email send
    print(f"\n  [SIMULATED EMAIL SENT]")
    print(f"  To      : {', '.join(stakeholders)}")
    print(f"  Subject : {subject}")
    print(f"  Files   : {[os.path.basename(f) for f in processed_files]}")
    logging.info(f"Email simulated to: {stakeholders} | Subject: {subject}")


# ── Main Pipeline ─────────────────────────────────────────────────────────────
def run_pipeline(day):
    """
    Master function that runs the full pipeline for a given day.
    Wednesday pipeline sends files on Thursday.
    Friday pipeline sends files on Monday.
    """
    print(f"\n{'='*60}")
    print(f"  Running Weekly Reporting Pipeline — {day.upper()} Files")
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

    cfg = CONFIG[day]

    # Step 1 — Pick files
    print(f"\n[Step 1] Picking files from: {cfg['input_folder']}")
    files = pick_files(cfg["input_folder"], cfg["file_keywords"])
    print(f"  Found {len(files)} file(s)")

    if not files:
        print("  No files found. Exiting pipeline.")
        return

    # Step 2 — Clean and process
    print(f"\n[Step 2] Cleaning and processing files...")
    processed = [clean_and_process(f, cfg["output_folder"]) for f in files]

    # Step 3 — Send email
    print(f"\n[Step 3] Sending email to stakeholders...")
    send_email(cfg["stakeholders"], cfg["email_subject"], processed)

    print(f"\n[COMPLETE] Pipeline finished in seconds.")
    print(f"  Files processed : {len(processed)}")
    print(f"  Stakeholders    : {cfg['stakeholders']}")
    logging.info(f"Pipeline complete for {day}. Files: {len(processed)}")


# ── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Generate sample data first
    print("Generating sample input files...")
    exec(open("generate_sample_data.py").read())

    # Run Wednesday pipeline (sends on Thursday)
    run_pipeline("wednesday")

    # Run Friday pipeline (sends on Monday)
    run_pipeline("friday")
