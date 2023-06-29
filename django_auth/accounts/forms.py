from datetime import timedelta

from django import forms
from django.forms import ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class UserCacheMixin:
    user_cache = None


class SignIn(UserCacheMixin, forms.Form):
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if settings.USE_REMEMBER_ME:
            self.fields['remember_me'] = forms.BooleanField(label=_('Remember me'), required=False)

    def clean_password(self):
        password = self.cleaned_data['password']

        if not self.user_cache:
            return password
        
        if not self.user_cache.check_password(password):
            raise ValidationError(_('You entered an invalid password.'))
        
        return password
    

class SignInViaUsernameForm(SignIn):
    username = forms.CharField(label=_('username'))
    
    @property
    def field_order(self):
        if settings.REMEMBER_ME:
            return ['username', 'password', 'remember_me']
        return ['username', 'password']
    
    def clean_username(self):
        username = self.cleaned_data['username']

        user = User.objects.filter(username=username).first()
        if not user:
            raise ValidationError(_('You entered an invalid username'))
        
        if not user.is_active:
            raise ValidationError(_('This account is no longer active'))
        
        self.user_cache = user

        return username


class EmailForm(UserCacheMixin, forms.Form):
    email = forms.EmailField(label=_('Email'))

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()

        if not user:
            raise ValidationError(_('You entered an invalid email address'))
        
        if not user.is_active:
            raise ValidationError(_('This account is no longer active'))


class SignInViaEmailForm(SignIn, EmailForm):
    @property
    def field_order(self):
        if settings.REMEMBER_ME:
            return ['username', 'password', 'remember_me']
        return ['username', 'password']


class EmailOrUsernameForm(UserCacheMixin, forms.Form):
    pass


class SignInViaEmailOrUsernameForm(SignIn, EmailOrUsernameForm):
    pass


class SignUpForm(UserCreationForm):
    pass

class ResendActivationCodeForm(UserCacheMixin, forms.Form):
    pass


class ResendActivationCodeViaEmailForm(UserCacheMixin, forms.Form):
    pass


class RestorePasswordForm(EmailForm):
    pass


class RestorePasswordViaEmailOrUsernameForm(EmailOrUsernameForm):
    pass


class ChangeProfileForm(forms.Form):
    pass


class ChangeEmailForm(forms.Form):
    pass


class RemindUsernameForm(EmailForm):
    pass