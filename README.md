# Automated Weekly Stakeholder Reporting Pipeline

## Overview
This automation handles the end-to-end process of picking up vendor index files, cleaning and processing them, and distributing the final reports to respective stakeholders automatically — with zero manual intervention.

## Problem Statement
Every Wednesday and Friday, two index data files were received from a vendor. These files needed to be:
- Downloaded and saved with proper index names
- Cleaned and delimited with commas
- Sent to respective stakeholders (Wednesday files on Thursday, Friday files on Monday)

This was a fully manual process taking significant time each week and was prone to human error.

## Solution
A Python automation that:
1. Picks files from a designated input folder (populated by Outlook rules)
2. Cleans and processes the data — removes duplicates, strips whitespace, handles missing values
3. Saves processed files with correct index names to an output folder
4. Automatically emails the files to respective stakeholders on the correct day

## Impact
- Runs twice weekly in under 10 seconds
- Zero manual intervention required
- Eliminated human errors in file naming, cleaning, and distribution
- Stakeholders receive files consistently and on time

## Project Structure
```
automation1_weekly_reporting/
├── weekly_reporting_automation.py   # Main automation script
├── generate_sample_data.py          # Generates dummy input files for demo
├── sample_input_files/              # Auto-generated sample CSV files
├── processed_files/                 # Output folder for processed files
└── weekly_reporting.log             # Auto-generated log file
```

## How to Run
```bash
# Install dependencies
pip install pandas openpyxl

# Run the automation (generates sample data and runs pipeline)
python weekly_reporting_automation.py
```

## Tools and Libraries
- Python 3.x
- pandas — data cleaning and processing
- openpyxl — Excel file handling
- smtplib — email distribution
- os, logging, datetime — file management and logging

## Note
This repository uses dummy data to demonstrate the automation logic.
The actual implementation was built for internal use at Morningstar India.
All company-specific API endpoints, credentials, and internal system
references have been replaced with generic placeholders.
