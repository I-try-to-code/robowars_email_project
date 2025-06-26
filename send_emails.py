import base64
import csv
import os
import time
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
ATTACHMENTS = ['Robowars Sponsorship Brochure .pdf', 'Robowars Marketing Brochure.pdf']
CC_EMAIL = 'robovitics@vit.ac.in'
RATE_LIMIT_SECONDS = 60

def gmail_authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def create_message(recipient, recipient_name, company_name):
    msg = EmailMessage()
    msg['To'] = recipient
    msg['From'] = "me"
    msg['Subject'] = "Robowars Sponsorship 2025 - VIT Vellore"
    msg['Cc'] = CC_EMAIL

    body = f"""
Respected {recipient_name},

We, RoboVITics, the premier robotics club of VIT Vellore, invite {company_name} to partner with us as a sponsor for Robowars 2025 — the flagship combat robotics event of GraVITas, VIT’s annual technical fest — scheduled during September 2025, with a footfall of over 40,000.

Robowars is South India’s largest combat robotics competition, where custom-built robots weighing 8 kg, 15 kg, and 60 kg battle in an arena designed for high-intensity action. The event attracts extensive media coverage, and participation from top engineering teams nationwide.

With participants from top engineering colleges nationwide, Robowars offers your brand unparalleled visibility among a diverse, tech-savvy audience. It’s a unique opportunity to showcase your brand on multiple media channels and engage with future innovators and decision-makers.

We have attached the sponsorship brochures outlining the benefits of collaboration. We’d love to discuss how we can collaborate. Please let us know a convenient time for a meeting.

Best regards,
RoboVITics
VIT Vellore
 
"""

    msg.set_content(body)

    for filepath in ATTACHMENTS:
        with open(filepath, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(filepath)
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    return {'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}

def send_mass_emails():
    service = gmail_authenticate()
    with open('contacts.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            to = row['email']
            name = row['recipient_name']
            company = row['company_name']
            print(f"Sending email to {name} at {company} ({to})...")
            try:
                message = create_message(to, name, company)
                service.users().messages().send(userId="me", body=message).execute()
                print("Email sent successfully.")
            except Exception as e:
                print(f"Failed to send email to {to}: {e}")
            print(f"Waiting {RATE_LIMIT_SECONDS} seconds to avoid spam detection...")
            time.sleep(RATE_LIMIT_SECONDS)

if __name__ == '__main__':
    send_mass_emails()
