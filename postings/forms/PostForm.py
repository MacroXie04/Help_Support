from django import forms
from django.utils import timezone

from postings.models import Post


class PostForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        ),
        help_text="Must be a future date and time.",
    )

    class Meta:
        model = Post
        fields = (
            "title",
            "description",
            "category",
            "max_accepted_applicants",
            "deadline",
        )
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 6}
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
            "max_accepted_applicants": forms.NumberInput(
                attrs={"class": "form-control", "min": 1}
            ),
        }

    # ----------------------------- #
    # Validation
    # ----------------------------- #
    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline and deadline <= timezone.now():
            raise forms.ValidationError("Deadline must be a future time.")
        return deadline

    def clean_max_accepted_applicants(self):
        num = self.cleaned_data.get("max_accepted_applicants")
        if num is not None and num < 1:
            raise forms.ValidationError("At least one applicant must be allowed.")
        return num
