import os
import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


class GmailProcessor:

    #
    service = None
    
    # The init method or constructor
    def __init__(self):

        # If modifying these scopes, delete the file token.json.
        SCOPES = [
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/gmail.compose",
            "https://mail.google.com/"
        ]

        # Try to log in to Gmail server 
        try:
            creds = None
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            current_dir = os.getcwd()
            work_dir= os.environ.get("WORK_DIR")
            token_path = f"{work_dir}/token.json"
            credn_path = f"{work_dir}/credentials.json"
            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(credn_path, SCOPES)
                    creds = flow.run_local_server(port=0)

                # Save the credentials for the next run
                with open(token_path, "w") as token:
                    token.write(creds.to_json()) 
            
            #
            GmailProcessor.service = build("gmail", "v1", credentials=creds)

        except Exception as e:
            # Print any error messages to stdout
            print(f"An error occurred: {e}")
        finally:
            pass

    @staticmethod
    def send(message: EmailMessage) -> str:
         # 3. Connect and send
        try:
            send_message = None
            with GmailProcessor.service as service:
                
                # encoded message
                encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

                create_message = {"raw": encoded_message}
                # pylint: disable=E1101
                send_message = (
                    service.users()
                    .messages()
                    .send(userId="me", body=create_message)
                    .execute()
                )
            if send_message is not None :    
                print(f'Email sent successfully with message id : {send_message["id"]}')
                return send_message["id"]
            else :    
                return None
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    GmailProcessor()
    # 2. Create the email content
    msg = EmailMessage()
    msg['Subject'] = "Testing Python Email"
    msg['From'] = "brijeshdhaker@gmail.com"
    msg['To'] = "brijeshdhaker@gmail.com"
    msg.set_content("This is a test email sent from a Python script!")

    GmailProcessor.send(msg)
