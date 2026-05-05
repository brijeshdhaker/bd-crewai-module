import os
import smtplib, ssl
from email.message import EmailMessage
from dotenv import load_dotenv

#
load_dotenv("/home/brijeshdhaker/IdeaProjects/bd-notebooks-module/.env")
#
if not os.environ.get("GOOGLE_SMTP_KEY"):
    os.environ["GOOGLE_SMTP_KEY"] = os.getenv("GOOGLE_SMTP_KEY")


def static_init(cls):
    if hasattr(cls, "__static_init__"):
        cls.__static_init__(cls)
    return cls

@static_init
class EamilProcessor:
    #
    server = None
    
    # 1. Setup email credentials and server details
    EMAIL_ADDRESS = "brijeshdhaker@gmail.com"
    EMAIL_PASSWORD = os.getenv("GOOGLE_SMTP_KEY")
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587  # Use 465 for SSL or 587 for TLS

    # The init method or constructor
    def __static_init__(cls):

        # Create a secure SSL context
        context = ssl.create_default_context()

        # Try to log in to server and send email
        try:
            cls.server = smtplib.SMTP(cls.SMTP_SERVER,cls.SMTP_PORT)
            cls.server.ehlo() # Can be omitted
            cls.server.starttls(context=context) # Secure the connection
            cls.server.ehlo() # Can be omitted
            cls.server.login(cls.EMAIL_ADDRESS, cls.EMAIL_PASSWORD)
            
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            pass

    @staticmethod
    def send(message: EmailMessage):
         # 3. Connect and send
        try:
            with EamilProcessor.server as smtp:
                smtp.send_message(message)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error: {e}")


# 2. Create the email content
msg = EmailMessage()
msg['Subject'] = "Testing Python Email"
msg['From'] = "brijeshdhaker@gmail.com"
msg['To'] = "brijeshdhaker@gmail.com"
msg.set_content("This is a test email sent from a Python script!")

EamilProcessor.send(msg)
