from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile
import datetime
import re


# User Registration Form
class UserRegisterForm(UserCreationForm):
    GENDER_CHOICES = [
        ('Abinary', 'Abinary'),
        ('Agender', 'Agender'),
        ('Ambigender', 'Ambigender'),
        ('Androgyne', 'Androgyne'),
        ('Androgynous', 'Androgynous'),
        ('Aporagender', 'Aporagender'),
        ('Autigender', 'Autigender'),
        ('Bakla', 'Bakla'),
        ('Bigender', 'Bigender'),
        ('Binary', 'Binary'),
        ('Bissu', 'Bissu'),
        ('Butch', 'Butch'),
        ('Calabai', 'Calabai'),
        ('Calalai', 'Calalai'),
        ('Cis', 'Cis'),
        ('Cisgender', 'Cisgender'),
        ('Cis female', 'Cis female'),
        ('Cis male', 'Cis male'),
        ('Cis man', 'Cis man'),
        ('Cis woman', 'Cis woman'),
        ('Demi-boy', 'Demi-boy'),
        ('Demiflux', 'Demiflux'),
        ('Demigender', 'Demigender'),
        ('Demi-girl', 'Demi-girl'),
        ('Demi-guy', 'Demi-guy'),
        ('Demi-man', 'Demi-man'),
        ('Demi-woman', 'Demi-woman'),
        ('Dual gender', 'Dual gender'),
        ('Eunuch', 'Eunuch'),
        ('Fa\'afafine', 'Fa\'afafine'),
        ('Female', 'Female'),
        ('Female to male', 'Female to male'),
        ('Femme', 'Femme'),
        ('FTM', 'FTM'),
        ('Gender bender', 'Gender bender'),
        ('Gender diverse', 'Gender diverse'),
        ('Gender gifted', 'Gender gifted'),
        ('Genderfae', 'Genderfae'),
        ('Genderfluid', 'Genderfluid'),
        ('Genderflux', 'Genderflux'),
        ('Genderfuck', 'Genderfuck'),
        ('Genderless', 'Genderless'),
        ('Gender nonconforming', 'Gender nonconforming'),
        ('Genderqueer', 'Genderqueer'),
        ('Gender questioning', 'Gender questioning'),
        ('Gender variant', 'Gender variant'),
        ('Graygender', 'Graygender'),
        ('Hijra', 'Hijra'),
        ('Intergender', 'Intergender'),
        ('Intersex', 'Intersex'),
        ('Ipsogender', 'Ipsogender'),
        ('Kathoey', 'Kathoey'),
        ('Māhū', 'Māhū'),
        ('Male', 'Male'),
        ('Male to female', 'Male to female'),
        ('Man of trans experience', 'Man of trans experience'),
        ('Maverique', 'Maverique'),
        ('Meta-gender', 'Meta-gender'),
        ('MTF', 'MTF'),
        ('Multigender', 'Multigender'),
        ('Muxe', 'Muxe'),
        ('Neither', 'Neither'),
        ('Neurogender', 'Neurogender'),
        ('Neutrois', 'Neutrois'),
        ('Non-binary', 'Non-binary'),
        ('Non-binary transgender', 'Non-binary transgender'),
        ('Omnigender', 'Omnigender'),
        ('Other', 'Other'),
        ('Pangender', 'Pangender'),
        ('Person of transgendered experience', 'Person of transgendered experience'),
        ('Polygender', 'Polygender'),
        ('Queer', 'Queer'),
        ('Sekhet', 'Sekhet'),
        ('Third gender', 'Third gender'),
        ('Trans', 'Trans'),
        ('Trans female', 'Trans female'),
        ('Trans male', 'Trans male'),
        ('Trans man', 'Trans man'),
        ('Trans person', 'Trans person'),
        ('Trans woman', 'Trans woman'),
        ('Transgender', 'Transgender'),
        ('Transgender female', 'Transgender female'),
        ('Transgender male', 'Transgender male'),
        ('Transgender man', 'Transgender man'),
        ('Transgender person', 'Transgender person'),
        ('Transgender woman', 'Transgender woman'),
        ('Transfeminine', 'Transfeminine'),
        ('Transmasculine', 'Transmasculine'),
        ('Transsexual', 'Transsexual'),
        ('Transsexual female', 'Transsexual female'),
        ('Transsexual male', 'Transsexual male'),
        ('Transsexual man', 'Transsexual man'),
        ('Transsexual person', 'Transsexual person'),
        ('Transsexual woman', 'Transsexual woman'),
        ('Travesti', 'Travesti'),
        ('Trigender', 'Trigender'),
        ('Tumtum', 'Tumtum'),
        ('Two spirit', 'Two spirit'),
    ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        required=False,
        label="Gender",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    first_name = forms.CharField(
        max_length=100,
        required=True,
        label="First Name",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        max_length=100,
        required=True,
        label="Last Name",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    phone = forms.CharField(
        max_length=15,
        required=True,
        label="Phone",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'gender', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        # Save the profile data in UserProfile
        user_profile = UserProfile(
            user=user,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            phone=self.cleaned_data['phone'],
            gender=self.cleaned_data['gender'],
        )

        if commit:
            user_profile.save()

        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )


from django import forms
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

        # 解析月份和年份，确保过期日期不能是过去的时间
        month, year = expiration_date.split('/')
        month = int(month)
        year = int(year)

        from datetime import datetime
        now = datetime.now()
        if year < now.year or (year == now.year and month < now.month):
            raise forms.ValidationError('The expiration date cannot be in the past.')

        return expiration_date