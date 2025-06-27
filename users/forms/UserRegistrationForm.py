# users/forms.py
import base64
from io import BytesIO

from PIL import Image
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

from users.models import UserProfile


class UserRegisterForm(UserCreationForm):
    COUNTRY_CHOICES = [
        ('', '--- Select Country ---'),
        ('KR', 'South Korea'),
        ('GB', 'United Kingdom'),
        ('US', 'United States'),
        ('CN', 'People\'s Republic of China'),
        ('TW', 'Republic of China'),
        ('JP', 'Japan'),
        ('CA', 'Canada'),
        ('AU', 'Australia'),
        ('DE', 'Germany'),
        ('FR', 'France'),
    ]

    GENDER_CHOICES = [
        ('', '--- Select Gender ---'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    # 重新添加first_name和last_name字段
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'})
    )

    phone_number = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'})
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    user_profile_img = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )

    class Meta:
        model = User
        # 将first_name和last_name添加回fields列表
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'gender', 'country', 'password_1',
                  'password_2', 'user_profile_img']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'password_1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'password_2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password_2'].help_text = None

        # 预先获取错误列表，避免在循环中重复访问
        field_errors = self.errors.keys()

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault('class', '')
                if 'form-select' not in field.widget.attrs['class']:
                    field.widget.attrs['class'] += ' form-select'
            else:
                field.widget.attrs.setdefault('class', '')
                if 'form-control' not in field.widget.attrs['class']:
                    field.widget.attrs['class'] += ' form-control'

            # 仅在有错误时添加is-invalid类
            if field_name in field_errors:
                field.widget.attrs['class'] += ' is-invalid'

    @transaction.atomic
    def save(self, commit=True):
        # 保存first_name和last_name到User模型
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

            # 处理图像
            img_file = self.cleaned_data['user_profile_img']
            base64_img = None

            if img_file:
                try:
                    with Image.open(img_file) as im:
                        min_side = min(im.size)
                        left = (im.width - min_side) // 2
                        top = (im.height - min_side) // 2

                        with im.crop((left, top, left + min_side, top + min_side)) as im_cropped:
                            im_resized = im_cropped.resize((128, 128), Image.LANCZOS)

                            buffer = BytesIO()
                            im_resized.save(buffer, format='PNG')
                            base64_img = base64.b64encode(buffer.getvalue()).decode('utf-8')
                except Exception as e:
                    self.add_error(None, "There was an error processing the uploaded image.")
                    return None

            # 创建UserProfile，只包含UserProfile模型中存在的字段
            UserProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                gender=self.cleaned_data['gender'],
                country=self.cleaned_data['country'],
                user_profile_img=base64_img,
            )

        return user