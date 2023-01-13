# #from celery import shared_task
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.template.loader import render_to_string
# from django.utils.encoding import force_bytes, force_str
# from django.core.mail import send_mail
# from .tokens import account_activation_token
# from django.conf import settings
# from .models import RegisteredUser
# from celery.utils.log import get_task_logger
#
# logger = get_task_logger(__name__)
#
#
# @shared_task
# def send_email_confirmation(user_id, domain):
#     logger.info('HERE 0')
#     user = RegisteredUser.objects.get(id=user_id)
#
#     mail_subject = 'Activation link has been sent to your email id'
#     logger.info('HERE 1')
#     message = render_to_string('account_activation_email.html', {
#         'user': user,
#         'domain': domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': account_activation_token.make_token(user)
#     })
#     to_email = user.email
#     is_mail_sent = send_mail(mail_subject, message, recipient_list=[to_email], from_email=settings.DEFAULT_FROM_EMAIL)
#
#     return is_mail_sent