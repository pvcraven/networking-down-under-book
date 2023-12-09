"""
Send e-mail using Mailtrap.
Get a free Mailtrap account at: https://mailtrap.io/
"""
import smtplib

sender = "Private Person <from@example.com>"
receiver = "A Test User <to@example.com>"

message = f"""\
Subject: Hi Mailtrap
To: {receiver}
From: {sender}

This is a test e-mail message."""

with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
    # When you sign up for Mailtrap, the service will
    # give you a login id and password that you need
    # to use below.
    server.login("01234567890abcd", "01234567890abcd")
    server.sendmail(sender, receiver, message)
