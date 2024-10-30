from django import forms
from django.contrib.auth.models import User
from index.models import HelpContent, SupportContent
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime


def clean_accept_time_limit(self):
    accept_time_limit = self.cleaned_data.get('accept_time_limit')
    if accept_time_limit:
        now = timezone.now()
        if accept_time_limit < now:
            raise forms.ValidationError("Accept time limit cannot be in the past.")
    return accept_time_limit


class ContentForm(forms.Form):
    COMMENT_TYPE_CHOICES = [
        ('Help', 'Help'),
        ('Support', 'Support')
    ]
    comment_type = forms.ChoiceField(choices=COMMENT_TYPE_CHOICES, label="Select the comment type")
    max_accept_user = forms.IntegerField(min_value=1, label="Max number of accept user", initial=1)
    total_money = forms.FloatField(min_value=0.0, label="Aggregate amount", required=True)
    accept_time_limit = forms.DateTimeField(label="Accept Limit Time", required=False,
                                            widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    content = forms.CharField(widget=forms.Textarea, label="Content", required=True)


class SuperUserDeleteForm(forms.Form):
    confirm_delete = forms.BooleanField(label="Confirm to delete the help content", required=True)

class AcceptHelpForm(forms.Form):
    confirm_request = forms.BooleanField(label="Confirm to request to accept the help content", required=True)