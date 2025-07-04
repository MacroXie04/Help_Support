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
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number'})
    )
    # MODIFIED: The image field is no longer strictly required on its own.
    user_profile_img = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )
    # NEW: Hidden field to store the Base64 data of the cropped image.
    cached_image_data = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'gender', 'country', 'email', 'phone_number', 'user_profile_img', 'cached_image_data']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Don't apply form-control to hidden inputs
            if not isinstance(field.widget, forms.HiddenInput):
                classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = (classes + ' form-control').strip()

                if self.errors.get(field_name):
                    field.widget.attrs['class'] += ' is-invalid'

    # NEW: Custom validation logic for the avatar.
    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('user_profile_img')
        cached_image = cleaned_data.get('cached_image_data')

        # An avatar is required, either as a new file or from the cache.
        if not image and not cached_image:
            self.add_error('user_profile_img', 'Please select an avatar.')

        return cleaned_data

    # MODIFIED: Updated save method to handle cached data and simplify image processing.
    def save(self, commit=True):
        # Save the User model first, but don't create the UserProfile yet.
        user = super().save(commit=False)

        # Assign names and email to the User object
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        base64_img = None
        img_file = self.cleaned_data.get('user_profile_img')
        cached_data = self.cleaned_data.get('cached_image_data')

        if img_file:
            # A new image was uploaded. The frontend already cropped it to a 128x128 PNG.
            # We just need to read it and encode it.
            img_file.seek(0)  # Go to the start of the file
            base64_img = base64.b64encode(img_file.read()).decode('utf-8')
        elif cached_data:
            # Use the cached Base64 data URL. We need to strip the metadata part.
            # e.g., "data:image/png;base64,iVBORw0KGgo..." -> "iVBORw0KGgo..."
            try:
                base64_img = cached_data.split(',')[1]
            except IndexError:
                # Fallback if the data is not a valid data URL, though it should be.
                base64_img = cached_data

        # Create the UserProfile with the final Base64 image data.
        if base64_img:
            UserProfile.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                gender=self.cleaned_data['gender'],
                country=self.cleaned_data['country'],
                email=self.cleaned_data['email'],
                phone_number=self.cleaned_data['phone_number'],
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
