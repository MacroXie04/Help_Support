# users/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    """
    Extends Django's built-in User model with additional profile information.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('User')
    )

    phone_number = models.CharField(
        max_length=20,
        blank=False,
        verbose_name=_('Phone Number')
    )

    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')

    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        blank=False,
        verbose_name=_('Gender')
    )

    class Country(models.TextChoices):
        SOUTH_KOREA = 'KR', _('South Korea')
        UNITED_KINGDOM = 'GB', _('United Kingdom')
        UNITED_STATES = 'US', _('United States')
        CHINA = 'CN', _('People\'s Republic of China')
        TAIWAN = 'TW', _('Republic of China')
        JAPAN = 'JP', _('Japan')
        CANADA = 'CA', _('Canada')
        AUSTRALIA = 'AU', _('Australia')
        GERMANY = 'DE', _('Germany')
        FRANCE = 'FR', _('France')

    country = models.CharField(
        max_length=2,
        choices=Country.choices,
        blank=False,
        verbose_name=_('Country')
    )

    user_profile_img = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Profile Image (Base64)')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_full_name(self):
        """Return the user's full name from the associated User model."""
        return self.user.get_full_name()

    def get_profile_image_url(self):
        """Return the data URL for the profile image if available."""
        if self.user_profile_img:
            return f"data:image/png;base64,{self.user_profile_img}"
        return None