from django import forms
from django.contrib.auth.models import User
from index.models import HelpContent, SupportContent
from django.core.exceptions import ValidationError
from django.utils import timezone

# make sure the time limit is in the future
def validate_future_time(value):
    if value <= timezone.now():
        raise ValidationError("The time limit must be in the future.")

class HelpContentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, required=True, label="content")
    time_limit = forms.DateTimeField(
        required=True,
        label="Time Limit",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        validators=[validate_future_time]
    )
    max_accept_user = forms.IntegerField(min_value=1, required=True, label="Maximum number of accepted users", initial=1)

    class Meta:
        model = HelpContent
        fields = ['content', 'time_limit', 'max_accept_user']


class SupportContentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, required=True, label="content")
    time_limit = forms.DateTimeField(
        required=True,
        label="Time Limit",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        validators=[validate_future_time]
    )
    max_accept_user = forms.IntegerField(min_value=1, required=True, label="Maximum number of accepted users", initial=1)

    class Meta:
        model = SupportContent
        fields = ['content', 'time_limit', 'max_accept_user']