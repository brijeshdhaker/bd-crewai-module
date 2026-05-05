#
# python src/main/py/com/example/agentic/mcp/emailserver.py
#
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from email.message import EmailMessage
from com.example.utils.GmailProcessor import GmailProcessor

# 1. Initialize FastMCP server
mcp = FastMCP("Email Notification MCP Server", port=8000)

# 2. Define Complex Data Type for Email
class EmailPayload(BaseModel):
    recipient: EmailStr
    subject: str
    body: str
    cc: Optional[List[EmailStr]] = Field(default=None, description="Optional CC list")
    attachment_names: Optional[List[str]] = Field(default=None, description="List of attachment filenames")
    params: Optional[dict[str, str]] = Field(description="Key-value pairs for templates")

GmailProcessor()

# 3. Define Tool with Complex Input
@mcp.tool()
def send_email(email: EmailPayload) -> str:
    """_summary_
    Sends a complex, structured email with CC and attachment metadata.
    Args:
        template: str
        params: dict
    Returns: 
        count of updated records
    Example:
        send an email notification with folloing details: 
        --recipient 'brijeshdhaker@gmail.com'
        --subject 'AI Notification Test #2025-01-01{id}'
        --body 'Hello {name},\n\n This is automated AI message send using AI Tools #Message-{id}'
        --params {"id":"2001", "name":"Brijesh"}
    """
    msg = EmailMessage()
    msg['From'] = "brijeshdhaker@gmail.com"
    msg['To'] = email.recipient
    
    #
    if email.cc:
        msg['Cc'] = ", ".join(email.cc)
    
    #
    _body = None
    if email.body and email.params:
        #_sql = request.template.format(**request.params)
        _body = email.body.format_map(email.params)
        msg['Subject'] = email.subject.format_map(email.params)
    else:
        _body = email.body
        msg['Subject'] = email.subject
    msg.set_content(_body)
    

    # Simulated Attachment Handling
    if email.attachment_names:
        return f"Drafted email to {email.recipient} with {len(email.attachment_names)} attachments: {email.attachment_names}"

    # --- SMTP Logic Here (e.g., using smtplib) ---
    return GmailProcessor.send(msg)

#
if __name__ == "__main__":
    mcp.run(transport="streamable-http")