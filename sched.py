import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import csv
from datetime import date

sender_email = 'sowmyanimmala11@gmail.com'
sender_password = 'aqbnjjxheczkfpcd'
smtp_server = 'smtp.gmail.com'
smtp_port = 587

def send_email():
    kl = read_csv_column("expDate.csv")

    current_date = date.today()
    print(current_date)



    for i in range(len(kl)):
        if(kl[i][1] == str(current_date)):

            recipient_email = kl[i][0]

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = 'Scheduled Email'

            # Add email body
            body = "This a remainder to change your account password since continuing with the same password may lead to some security issues"
            msg.attach(MIMEText(body, 'plain'))

            # Add an attachment (optional)
            # with open('attachment.pdf', 'rb') as attachment:
            #     part = MIMEApplication(attachment.read(), Name='attachment.pdf')
            #     part['Content-Disposition'] = f'attachment; filename="attachment.pdf"'
            #     msg.attach(part)

            # Connect to the SMTP server and send the email
            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
                server.quit()
                print('Email sent successfully!')
           except Exception as e:
              print(f'Error sending email: {e}')


def read_csv_column(csv_file):
    column_values = []

    with open(csv_file, 'r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            column_values.append([row["Email"], row["ExpDate"]])

    return column_values

schedule.every().day.at('23:15').do(send_email)

while True:
    schedule.run_pending()
    time.sleep(1)

