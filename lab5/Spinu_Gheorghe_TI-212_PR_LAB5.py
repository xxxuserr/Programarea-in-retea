import imaplib
import poplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

EMAIL = "your-email@gmail.com"
PASSWORD = "your-password"

def list_emails_imap():
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(EMAIL, PASSWORD)
        mail.select('inbox')
        
        result, data = mail.search(None, 'ALL')
        email_ids = data[0].split()
        
        for e_id in email_ids:
            result, msg_data = mail.fetch(e_id, '(RFC822)')
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            print(f"From: {msg['from']}")
            print(f"Subject: {msg['subject']}")
            print("-" * 50)
            
        mail.logout()
    except Exception as e:
        print(f"IMAP Error: {e}")

def list_emails_pop3():
    try:
        mail = poplib.POP3_SSL('pop.gmail.com')
        mail.user(EMAIL)
        mail.pass_(PASSWORD)
        
        num_messages = len(mail.list()[1])
        
        for i in range(num_messages):
            response, lines, octets = mail.retr(i + 1)
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            msg = email.message_from_string(msg_content)
            
            print(f"From: {msg['from']}")
            print(f"Subject: {msg['subject']}")
            print("-" * 50)
        
        mail.quit()
    except Exception as e:
        print(f"POP3 Error: {e}")

def download_email_with_attachments(email_id, save_path):
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(EMAIL, PASSWORD)
        mail.select('inbox')
        
        result, msg_data = mail.fetch(email_id, '(RFC822)')
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            file_name = part.get_filename()
            if bool(file_name):
                file_path = os.path.join(save_path, file_name)
                with open(file_path, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                print(f"Downloaded {file_name}")
        
        mail.logout()
    except Exception as e:
        print(f"Download Error: {e}")

def send_email(subject, body, to, reply_to=None):
    try:
        msg = MIMEText(body)
        msg['From'] = EMAIL
        msg['To'] = to
        msg['Subject'] = subject
        if reply_to:
            msg.add_header('reply-to', reply_to)
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, to, msg.as_string())
        server.quit()
        
        print("Email sent successfully.")
    except Exception as e:
        print(f"Send Email Error: {e}")

def send_email_with_attachment(subject, body, to, file_path, reply_to=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = to
        msg['Subject'] = subject
        if reply_to:
            msg.add_header('reply-to', reply_to)
        
        msg.attach(MIMEText(body, 'plain'))
        
        attachment = open(file_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(file_path)}')
        
        msg.attach(part)
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, to, msg.as_string())
        server.quit()
        
        print("Email with attachment sent successfully.")
    except Exception as e:
        print(f"Send Email with Attachment Error: {e}")

# Exemplu de utilizare:
if __name__ == "__main__":
    print("1. Lista de email-uri cu IMAP")
    print("2. Lista de email-uri cu POP3")
    print("3. Descarcă email cu atașamente")
    print("4. Trimite email text")
    print("5. Trimite email cu atașament")
    
    choice = input("Introduceti optiunea dvs.: ")
    
    if choice == "1":
        list_emails_imap()
    elif choice == "2":
        list_emails_pop3()
    elif choice == "3":
        email_id = input("Introduceti ID-ul email-ului: ")
        save_path = input("Introduceti calea de salvare a atașamentelor: ")
        download_email_with_attachments(email_id, save_path)
    elif choice == "4":
        to = input("Introduceti adresa de email a destinatarului: ")
        subject = input("Introduceti subiectul: ")
        body = input("Introduceti corpul email-ului: ")
        reply_to = input("Introduceti adresa de reply-to (optional): ")
        send_email(subject, body, to, reply_to if reply_to else None)
    elif choice == "5":
        to = input("Introduceti adresa de email a destinatarului: ")
        subject = input("Introduceti subiectul: ")
        body = input("Introduceti corpul email-ului: ")
        file_path = input("Introduceti calea fisierului atașat: ")
        reply_to = input("Introduceti adresa de reply-to (optional): ")
        send_email_with_attachment(subject, body, to, file_path, reply_to if reply_to else None)
    else:
        print("Opțiune invalidă.")
