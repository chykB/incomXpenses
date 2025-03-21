from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_activation_email(to_email, activation_url, username):
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=to_email,
        subject="Please Activate Your Account",
        html_content=f'''
            <h3>Hello {username}</h3>
            <p>Please click the link below to activate your account</p>
            <p><a href="{activation_url}">Activate</a></p>
            <p>This link expires in 24 hours</p>
        '''
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code == 202
    except Exception as e:
        print(e)
        return False