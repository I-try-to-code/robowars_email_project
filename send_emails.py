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

def create_message(to, name, company):
    msg = EmailMessage()
    msg['To'] = to
    msg['From'] = 'me'
    msg['Cc'] = CC_EMAIL
    msg['Subject'] = f" Robowars Sponsorship 2025 - VIT Vellore "

    # --- HTML Email Body ---
    html_body = f"""
    <html>
    <body>
    <p>Respected {name},</p>

    <p>
    We, RoboVITics, the premier robotics club of VIT Vellore invite 
    {company} to partner with us as a sponsor for <strong>RoboWars 2025, the 
    flagship combat robotics event of GraVITas</strong>, VIT’s annual technical fest, scheduled for 
    September 2025 with an expected <strong>footfall of over 40,000.</strong>
    </p>

    <p>
    <strong>RoboWars</strong> is South India’s largest combat robotics competition, where custom-built robots 
    weighing <strong>8 kg, 15 kg, and 60 kg</strong> battle in a high-intensity arena. 
    The event draws extensive media coverage and participation from top engineering teams 
    across the nation.
    </p>

    <p>
    With participants from leading engineering colleges, RoboWars offers your brand 
    unparalleled visibility among a diverse, tech-savvy audience. This is a unique opportunity to 
    showcase your brand across multiple media platforms and connect with future 
    innovators and decision-makers.
    </p>

    <p>
    We have attached our sponsorship brochures outlining the benefits of collaboration. 
    We’d be happy to discuss how we can work together. Kindly let us know a convenient 
    time for a meeting.
    </p>

    <p>
    Best regards,<br>
    RoboVITics<br>
    VIT Vellore
    </p>
    </body>
    </html>
    """

    # --- Use HTML body ---
    msg.set_content("This is an HTML email. Please view it in an HTML-compatible mail client.")
    msg.add_alternative(html_body, subtype='html')

    # --- Add attachments ---
    for file in ATTACHMENTS:
        with open(file, 'rb') as f:
            data = f.read()
            msg.add_attachment(data, maintype='application', subtype='octet-stream', filename=os.path.basename(file))

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
