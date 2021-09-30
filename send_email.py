import smtplib
from email.mime.text import MIMEText

def send_email(email, destination, weight, price):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '2b2d31c43838d5'
    password = '047b59a5fcea8f'
    message = f"<h3>New Quote Request</h3><ul><li>Destination: {destination}</li><li>Parcel weight: {weight}</li></ul><h4>Total shipment cost: ${price}</h4>"

    sender = 'noreply@planex.com'
    receiver = email
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Request for Planet Express Shipment Quote'
    msg['From'] = sender
    msg['To'] = receiver

    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender, receiver, msg.as_string())
