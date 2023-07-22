from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import  gettext_lazy as _


def send_mail(to, template, context):
    html_context = render_to_string(f'accounts/emails/{template}.html', context)
    text_context = render_to_string(f'accounts/email{template}.txt', context)

    msg = EmailMultiAlternatives(context['subject'], text_context, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(html_context, 'text/html')
    msg.send()

def send_activation_email(request, email, code):
    context = {
        'subject': _('Account activation'),
        'uri': request.build_absolute_uri(reverse('accounts:activate', kwargs={'code': code})),
    }

    send_mail(email, 'activate_account', context)
    