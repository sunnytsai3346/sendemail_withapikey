from flask import Flask, request, jsonify, abort
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

FROM_EMAIL = os.getenv("FROM_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")
API_KEY = os.getenv("API_KEY")  # The API key for authentication

def send_contact_email(to_email, subject, html_content, from_email, password):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

    try:
        # Connect to the Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)

        # Send the email
        server.sendmail(from_email, to_email, msg.as_string())

        # Close the connection
        server.quit()

        return "Email sent successfully!"

    except smtplib.SMTPException as e:
        return f"SMTP error: {e}"

    except Exception as e:
        return f"Unexpected error: {e}"

def authenticate_request(api_key):
    """Check if the provided API key matches the expected key."""
    return api_key == API_KEY

@app.route('/api/send_email', methods=['POST'])
def send_email():
    # Authenticate the request using the API key
    api_key = request.headers.get('x-api-key')
    if not api_key or not authenticate_request(api_key):
        return jsonify({'error': 'Unauthorized access'}), 401

    # Process the request body
    data = request.json
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    name = data.get('name')
    email = data.get('sender_email')
    message = data.get('message')

    if not all([name, email, message]):
        return jsonify({'error': 'Missing required fields: name, sender_email, or message'}), 400

    if '@' not in email:
        return jsonify({'error': 'Invalid email address'}), 400

    subject = f"{email} - {name}"

    html_content = f"""
    <h2>New Contact Request</h2>
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Message:</strong> {message}</p>
    """

    result = send_contact_email(TO_EMAIL, subject, html_content, FROM_EMAIL, APP_PASSWORD)

    if "Error" in result:
        return jsonify({'error': result}), 500

    return jsonify({'message': result})

if __name__ == '__main__':
    app.run(debug=True)
