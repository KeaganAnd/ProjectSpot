import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

# Load environment variables from keys.env
load_dotenv(dotenv_path="keys.env")

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")  

def send_verification_email(to_email, code):
    """
    Send a verification code to the user's email using SendGrid.
    
    Args:
        to_email (str): Receiver's email address.
        code (str): Verification code to send.

    Returns:
        bool: True if sent successfully, False otherwise.
    """
    if not SENDGRID_API_KEY:
        print("❌ SENDGRID_API_KEY missing in environment.")
        return False
    if not SENDER_EMAIL:
        print("❌ SENDER_EMAIL missing in environment.")
        return False

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        message = Mail(
            from_email=SENDER_EMAIL,
            to_emails=to_email,
            subject="Your SpotFinder Verification Code",
            html_content=f"""
                <p>Hello,</p>
                <p>Your SpotFinder verification code is:</p>
                <h2>{code}</h2>
                <p>This code will expire in 10 minutes. Do not share it with anyone.</p>
                <p>If you did not request this, you can safely ignore this email.</p>
            """
        )
        response = sg.send(message)
        print(f"[SendGrid] Status: {response.status_code}")
        return response.status_code == 202

    except Exception as e:
        print(f"[SendGrid] Error: {e}")
        return False
