import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""With this function we send out our HTML email"""

TO = "pradeeshwar10@gmail.com"
FROM = "mtech339@gmail.com"

BODY = """

<h1>Transfer Certificate Request Verification</h1>
<a href="www.google.com">Authorize Request</a>
<a href="www.google.com">Deny Request</a>

"""

def send_mail(TO, FROM, BODY):
    # Create message container - the correct MIME type is multipart/alternative here!
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = "SUBJECT"
    MESSAGE['To'] = TO
    MESSAGE['From'] = FROM
    MESSAGE.preamble = """
    Your mail reader does not support the report format.
    Please visit us online!"""

    # Record the MIME type text/html.
    HTML_BODY = MIMEText(BODY, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    MESSAGE.attach(HTML_BODY)

    # The actual sending of the e-mail
    server = smtplib.SMTP('smtp.gmail.com:587')

    # Credentials (if needed) for sending the mail
    password = "cmewcdgbvisfjfph"

    server.starttls()
    server.login(FROM,password)
    server.sendmail(FROM, [TO], MESSAGE.as_string())
    server.quit()

    return True