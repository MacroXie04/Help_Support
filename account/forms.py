from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile
import datetime
import re


class PaymentForm(forms.Form):
    card_number = forms.CharField(
        label='Card Number',
        max_length=16,
        min_length=16,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your card number', 'class': 'form-control rounded-xs'}),
        error_messages={
            'required': 'Please enter your card number',
            'min_length': 'Card number must be 16 digits',
            'max_length': 'Card number must be 16 digits'
        }
    )

    # 修改过期日期字段为字符串，并使用正则表达式验证格式为MM/YYYY
    expiration_date = forms.CharField(
        label='Expiration Date (MM/YYYY)',
        widget=forms.TextInput(attrs={'placeholder': 'MM/YYYY', 'class': 'form-control rounded-xs'}),
        error_messages={'required': 'Please enter the expiration date'}
    )

    security_code = forms.CharField(
        label='Security Code',
        max_length=3,
        min_length=3,
        widget=forms.TextInput(attrs={'placeholder': 'Enter CVV', 'class': 'form-control rounded-xs'}),
        error_messages={
            'required': 'Please enter your CVV',
            'min_length': 'CVV must be 3 digits',
            'max_length': 'CVV must be 3 digits'
        }
    )

    amount = forms.DecimalField(
        label='Amount',
        min_value=0.01,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter amount', 'class': 'form-control rounded-xs'}),
        error_messages={'required': 'Please enter an amount', 'min_value': 'Amount must be greater than 0'}
    )

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data['expiration_date']
        if not re.match(r'^(0[1-9]|1[0-2])\/\d{4}$', expiration_date):
            raise forms.ValidationError('Please enter a valid expiration date in MM/YYYY format.')

        month, year = expiration_date.split('/')
        month = int(month)
        year = int(year)

        from datetime import datetime
        now = datetime.now()
        if year < now.year or (year == now.year and month < now.month):
            raise forms.ValidationError('The expiration date cannot be in the past.')

        return expiration_date