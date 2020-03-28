import smtplib
import ssl

port = 587  # For starttls
smtp_server = "smtp.zoho.com"
sender_email = "rajat.saini@alervice.com"
receiver_email = "pshkmr007@gmail.com"
password = 'R@jat#111'
message = """\
Subject: Hi there

This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
