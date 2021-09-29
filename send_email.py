import smtplib
from email.mime.text import MIMEText

def send_email(email, destination, weight):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '2b2d31c43838d5'
    password = '047b59a5fcea8f'
    message = f"<h3>New Quote Request</h3><br><ul><li>Email: {email}</li><li>Destination: {destination}</li><li>Parcel weight: {weight}</li></ul>"

    sender_email = 'noreply@planex.com'
    receiver_email = 'name@mail.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Request for Planet Express Shipment Quote'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
