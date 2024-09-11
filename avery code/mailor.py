import yagmail
import smtplib, ssl
import csv
import math, random

def otp(email):
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    otp = OTP

    # port = 465  # For SSL
    # smtp_server = "smtp.gmail.com"
    # sender_email = "f20200002@pilani.bits-pilani.ac.in"  # Enter your address
    # receiver_email = email  # Enter receiver address
    # password = "gnifreshcdjpcttc"
    # Subject = "Subject: Otp For verification"
    # Body="Body: This is your otp: " + otp

    # context = ssl.create_default_context()
    # with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    #     server.login(sender_email, password)
    #     server.sendmail(sender_email, receiver_email, Subject,Body)
    rows = [otp]

    email = email
    yag = yagmail.SMTP('f20200002@pilani.bits-pilani.ac.in', 'gnifreshcdjpcttc')
    Subject = "Subject: Otp For verification"
    Body = "Body: This is your otp: " + otp
    yag.send(email, 'One-Time Password OTP',Body)
    rows = [otp]
    with open('file.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(rows)
        csvfile.close()