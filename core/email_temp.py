from django.template.loader import render_to_string
from core.utils import generate_otp, generate_username
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import jwt
from core.utils import send_email
from django.conf import settings
from account.models import PasswordReset, Profile
from django.contrib.auth.models import User

def send_welcome_email(user_email):
    mail_subject = "Welcome"
    link_address = settings.BASE_URL+"reset-password/?token="
    mail_body = render_to_string('email_templates/welcome_mail.html', {'link': link_address})
    data ={
        'subject':mail_subject,
        'body':mail_body,
        'email':user_email
    }
    send_email(data)

def send_password_reset_email(email):
    try:
        userObj = User.objects.get(email=email)
        otp, expiry,token = generate_otp(email)
        pswd = PasswordReset.objects.get(user=userObj, valid_til__gt = timezone.now(), password_updated=False)
        payload = jwt.decode(token, 'your-secret-key', algorithms=['HS256'])
        uemail = payload['email']
        otp = payload['otp']
        exp = payload['exp']
        
        mail_subject = "Password Reset Email"
        link_address = settings.BASE_URL+"ac/reset-password/?token="+token
        mail_body = render_to_string('email_templates/password_reset_with_otp.html', {'link': link_address, 'otp':otp})
        data ={
            'subject':mail_subject,
            'body':mail_body,
            'email':email
        }
        send_email(data)
        pswd.otp = otp
        pswd.save()
        # messages.success(request, 'Password reset email sent')

    except PasswordReset.DoesNotExist:
        mail_subject = "Password Reset Email"
        link_address = settings.BASE_URL+"ac/reset-password/?token="+token
        mail_body = render_to_string('email_templates/password_reset_with_otp.html', {'link': link_address, 'otp':otp})
        data ={
            'subject':mail_subject,
            'body':mail_body,
            'email':email
        }
        # send email with password reset token
        send_email(data)
        PasswordReset.objects.create(user=userObj, otp=otp, valid_til=expiry,token=token)
        # messages.success(request, 'Password reset email sent')
    # return redirect(reverse('account:forgot-password'))