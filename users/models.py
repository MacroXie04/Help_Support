from django.db import models
from django.contrib.auth.models import User

COUNTRY_CHOICES = [
    # Asia
    ('cn', 'China'),
    ('jp', 'Japan'),
    ('kr', 'South Korea'),
    ('in', 'India'),
    ('id', 'Indonesia'),
    ('my', 'Malaysia'),
    ('ph', 'Philippines'),
    ('th', 'Thailand'),
    ('vn', 'Vietnam'),
    ('sg', 'Singapore'),
    ('tw', 'Taiwan'),
    ('hk', 'Hong Kong'),
    ('mo', 'Macau'),
    ('ae', 'United Arab Emirates'),
    ('sa', 'Saudi Arabia'),
    ('il', 'Israel'),
    ('tr', 'Turkey'),
    ('pk', 'Pakistan'),
    ('bd', 'Bangladesh'),
    ('lk', 'Sri Lanka'),

    # Europe
    ('gb', 'United Kingdom'),
    ('de', 'Germany'),
    ('fr', 'France'),
    ('es', 'Spain'),
    ('it', 'Italy'),
    ('ru', 'Russia'),
    ('nl', 'Netherlands'),
    ('be', 'Belgium'),
    ('ch', 'Switzerland'),
    ('se', 'Sweden'),
    ('no', 'Norway'),
    ('dk', 'Denmark'),
    ('fi', 'Finland'),
    ('at', 'Austria'),
    ('pl', 'Poland'),
    ('pt', 'Portugal'),
    ('gr', 'Greece'),
    ('hu', 'Hungary'),
    ('cz', 'Czech Republic'),
    ('ro', 'Romania'),

    # North America
    ('us', 'United States'),
    ('ca', 'Canada'),
    ('mx', 'Mexico'),
    ('pr', 'Puerto Rico'),
    ('gt', 'Guatemala'),
    ('cu', 'Cuba'),

    # South America
    ('br', 'Brazil'),
    ('ar', 'Argentina'),
    ('co', 'Colombia'),
    ('pe', 'Peru'),
    ('mx', 'Mexico'),
    ('ve', 'Venezuela'),
    ('cl', 'Chile'),

    ('au', 'Australia'),
    ('nz', 'New Zealand'),
    ('pg', 'Papua New Guinea'),

    ('ng', 'Nigeria'),
    ('eg', 'Egypt'),
    ('za', 'South Africa'),
    ('ke', 'Kenya'),
    ('ma', 'Morocco'),
    ('dz', 'Algeria'),

    # Other
    ('other', 'Other'),
]


GENDER_CHOICES = [
    # Common binary and trans identities
    ('male', 'Male'),
    ('female', 'Female'),
    ('cis_male', 'Cis Male'),
    ('cis_female', 'Cis Female'),
    ('trans_male', 'Trans Male'),
    ('trans_female', 'Trans Female'),
    ('trans_man', 'Trans Man'),
    ('trans_woman', 'Trans Woman'),
    ('ftm', 'FTM (Female to Male)'),
    ('mtf', 'MTF (Male to Female)'),

    # Non-binary umbrella
    ('non_binary', 'Non-Binary'),
    ('genderqueer', 'Genderqueer'),
    ('genderfluid', 'Genderfluid'),
    ('agender', 'Agender'),
    ('bigender', 'Bigender'),
    ('demiboy', 'Demiboy'),
    ('demigirl', 'Demigirl'),
    ('genderflux', 'Genderflux'),
    ('androgyne', 'Androgyne'),
    ('neutrois', 'Neutrois'),
    ('pangender', 'Pangender'),
    ('polygender', 'Polygender'),
    ('trigender', 'Trigender'),
    ('maverique', 'Maverique'),
    ('two_spirit', 'Two-Spirit'),
    ('third_gender', 'Third Gender'),
    ('xenogender', 'Xenogender'),
    ('autigender', 'Autigender'),
    ('apora_gender', 'Aporagender'),
    ('caelgender', 'Caelgender'),
    ('juxera', 'Juxera'),
    ('egogender', 'Egogender'),
    ('genderblank', 'Genderblank'),
    ('genderfree', 'Genderfree'),
    ('genderless', 'Genderless'),
    ('quoisgender', 'Quoigender'),
    ('omnigender', 'Omnigender'),
    ('intergender', 'Intergender'),
    ('graygender', 'Graygender'),

    # Cultural / regional gender categories
    ('hijra', 'Hijra'),
    ('bakla', 'Bakla'),
    ('bissu', 'Bissu'),
    ('faafafine', 'Faʻafafine'),
    ('mahu', 'Māhū'),
    ('muxe', 'Muxe'),
    ('kathoey', 'Kathoey'),
    ('waria', 'Waria'),
    ('winkte', 'Winkte'),
    ('vakasalewalewa', 'Vakasalewalewa'),
    ('calabai', 'Calabai'),
    ('calalai', 'Calalai'),

    # Other/expanded
    ('butch', 'Butch'),
    ('femme', 'Femme'),
    ('transfeminine', 'Transfeminine'),
    ('transmasculine', 'Transmasculine'),
    ('transandrogynous', 'Transandrogynous'),
    ('eunuch', 'Eunuch'),
    ('person_of_trans_experience', 'Person of Trans Experience'),
    ('gender_nonconforming', 'Gender Nonconforming'),
    ('gender_variant', 'Gender Variant'),
    ('gender_bender', 'Gender Bender'),
    ('questioning', 'Questioning'),
    ('other', 'Other'),
    ('prefer_not_to_say', 'Prefer not to say'),
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)

    # Base64-encoded PNG image (128x128)
    profile_image_base64 = models.TextField(help_text="Base64 encoded PNG image (128x128)")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username})"


class UserAccountAuthentication(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='authentication')

    account_disabled = models.BooleanField(default=False, help_text="Indicates if the account is disabled")

    def __str__(self):
        return f"Authentication for {self.user.username}"