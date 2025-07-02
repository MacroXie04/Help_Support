import base64
from io import BytesIO

from PIL import Image
from django import forms

from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)

from django.contrib.auth.models import User

from users.models import UserProfile


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last name'})
    )
    gender = forms.ChoiceField(
        choices=UserProfile._meta.get_field('gender').choices,
        widget=forms.Select()
    )
    country = forms.ChoiceField(
        choices=UserProfile._meta.get_field('country').choices,
        widget=forms.Select()
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email address'})
    )
    user_profile_img = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'gender', 'country', 'email', 'user_profile_img']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (classes + ' form-control').strip()

            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'

    def save(self, commit=True):
        # Save the User model first
        user = super().save(commit=commit)

        # Get additional profile fields
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        gender = self.cleaned_data['gender']
        country = self.cleaned_data['country']
        email = self.cleaned_data['email']
        img_file = self.cleaned_data['user_profile_img']

        # Assign names and email to User
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if commit:
            user.save()

        # Process image to 128x128 Base64 PNG
        with Image.open(img_file) as im:
            min_side = min(im.size)
            left = (im.width - min_side) // 2
            top = (im.height - min_side) // 2
            im = im.crop((left, top, left + min_side, top + min_side))
            im = im.resize((128, 128), Image.LANCZOS)

            buffer = BytesIO()
            im.save(buffer, format='PNG')
            base64_img = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # Create UserProfile instance
        UserProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            country=country,
            email=email,
            profile_image_base64=base64_img,
        )

        return user


# UserLoginForm
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username'
            }
        )
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'
