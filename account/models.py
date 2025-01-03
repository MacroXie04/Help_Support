from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # link to user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # account static
    is_verified = models.BooleanField(default=False)

    # contact info
    phone_area_code = models.CharField(max_length=3)
    phone = models.CharField(max_length=15)

    # one time code
    login_protect = models.BooleanField(default=False)

    # time zone
    TIME_ZONE = (
        ('GMT-12:00', 'International Date Line West'),
        ('GMT-11:00', 'American Samoa'),
        ('GMT-11:00', 'Midway Island'),
        ('GMT-10:00', 'Hawaii'),
        ('GMT-09:00', 'Alaska'),
        ('GMT-08:00', 'Pacific Time (US & Canada)'),
        ('GMT-08:00', 'Tijuana'),
        ('GMT-07:00', 'Arizona'),
        ('GMT-07:00', 'Mazatlan'),
        ('GMT-07:00', 'Mountain Time (US & Canada)'),
        ('GMT-06:00', 'Central America'),
        ('GMT-06:00', 'Central Time (US & Canada)'),
        ('GMT-06:00', 'Chihuahua'),
        ('GMT-06:00', 'Guadalajara'),
        ('GMT-06:00', 'Mexico City'),
        ('GMT-06:00', 'Monterrey'),
        ('GMT-06:00', 'Saskatchewan'),
        ('GMT-05:00', 'Bogota'),
        ('GMT-05:00', 'Eastern Time (US & Canada)'),
        ('GMT-05:00', 'Indiana (East)'),
        ('GMT-05:00', 'Lima'),
        ('GMT-05:00', 'Quito'),
        ('GMT-04:00', 'Atlantic Time (Canada)'),
        ('GMT-04:00', 'Caracas'),
        ('GMT-04:00', 'Georgetown'),
        ('GMT-04:00', 'La Paz'),
        ('GMT-04:00', 'Puerto Rico'),
        ('GMT-04:00', 'Santiago'),
        ('GMT-03:30', 'Newfoundland'),
        ('GMT-03:00', 'Brasilia'),
        ('GMT-03:00', 'Buenos Aires'),
        ('GMT-03:00', 'Montevideo'),
        ('GMT-02:00', 'Greenland'),
        ('GMT-02:00', 'Mid-Atlantic'),
        ('GMT-01:00', 'Azores'),
        ('GMT-01:00', 'Cape Verde Is.'),
        ('GMT+00:00', 'Edinburgh'),
        ('GMT+00:00', 'Lisbon'),
        ('GMT+00:00', 'London'),
        ('GMT+00:00', 'Monrovia'),
        ('GMT+00:00', 'UTC'),
        ('GMT+01:00', 'Amsterdam'),
        ('GMT+01:00', 'Belgrade'),
        ('GMT+01:00', 'Berlin'),
        ('GMT+01:00', 'Bern'),
        ('GMT+01:00', 'Bratislava'),
        ('GMT+01:00', 'Brussels'),
        ('GMT+01:00', 'Budapest'),
        ('GMT+01:00', 'Casablanca'),
        ('GMT+01:00', 'Copenhagen'),
        ('GMT+01:00', 'Dublin'),
        ('GMT+01:00', 'Ljubljana'),
        ('GMT+01:00', 'Madrid'),
        ('GMT+01:00', 'Paris'),
        ('GMT+01:00', 'Prague'),
        ('GMT+01:00', 'Rome'),
        ('GMT+01:00', 'Sarajevo'),
        ('GMT+01:00', 'Skopje'),
        ('GMT+01:00', 'Stockholm'),
        ('GMT+01:00', 'Vienna'),
        ('GMT+01:00', 'Warsaw'),
        ('GMT+01:00', 'West Central Africa'),
        ('GMT+01:00', 'Zagreb'),
        ('GMT+01:00', 'Zurich'),
        ('GMT+02:00', 'Athens'),
        ('GMT+02:00', 'Bucharest'),
        ('GMT+02:00', 'Cairo'),
        ('GMT+02:00', 'Harare'),
        ('GMT+02:00', 'Helsinki'),
        ('GMT+02:00', 'Jerusalem'),
        ('GMT+02:00', 'Kaliningrad'),
        ('GMT+02:00', 'Kyiv'),
        ('GMT+02:00', 'Pretoria'),
        ('GMT+02:00', 'Riga'),
        ('GMT+02:00', 'Sofia'),
        ('GMT+02:00', 'Tallinn'),
        ('GMT+02:00', 'Vilnius'),
        ('GMT+03:00', 'Baghdad'),
        ('GMT+03:00', 'Istanbul'),
        ('GMT+03:00', 'Kuwait'),
        ('GMT+03:00', 'Minsk'),
        ('GMT+03:00', 'Moscow'),
        ('GMT+03:00', 'Nairobi'),
        ('GMT+03:00', 'Riyadh'),
        ('GMT+03:00', 'St. Petersburg'),
        ('GMT+03:00', 'Volgograd'),
        ('GMT+03:30', 'Tehran'),
        ('GMT+04:00', 'Abu Dhabi'),
        ('GMT+04:00', 'Baku'),
        ('GMT+04:00', 'Muscat'),
        ('GMT+04:00', 'Samara'),
        ('GMT+04:00', 'Tbilisi'),
        ('GMT+04:00', 'Yerevan'),
        ('GMT+04:30', 'Kabul'),
        ('GMT+05:00', 'Almaty'),
        ('GMT+05:00', 'Astana'),
        ('GMT+05:00', 'Ekaterinburg'),
        ('GMT+05:00', 'Islamabad'),
        ('GMT+05:00', 'Karachi'),
        ('GMT+05:00', 'Tashkent'),
        ('GMT+05:30', 'Chennai'),
        ('GMT+05:30', 'Kolkata'),
        ('GMT+05:30', 'Mumbai'),
        ('GMT+05:30', 'New Delhi'),
        ('GMT+05:30', 'Sri Jayawardenepura'),
        ('GMT+05:45', 'Kathmandu'),
        ('GMT+06:00', 'Dhaka'),
        ('GMT+06:00', 'Urumqi'),
        ('GMT+06:30', 'Rangoon'),
        ('GMT+07:00', 'Bangkok'),
        ('GMT+07:00', 'Hanoi'),
        ('GMT+07:00', 'Jakarta'),
        ('GMT+07:00', 'Krasnoyarsk'),
        ('GMT+07:00', 'Novosibirsk'),
        ('GMT+08:00', 'Beijing'),
        ('GMT+08:00', 'Chongqing'),
        ('GMT+08:00', 'Hong Kong'),
        ('GMT+08:00', 'Irkutsk'),
        ('GMT+08:00', 'Kuala Lumpur'),
        ('GMT+08:00', 'Perth'),
        ('GMT+08:00', 'Singapore'),
        ('GMT+08:00', 'Taipei'),
        ('GMT+08:00', 'Ulaanbaatar'),
        ('GMT+09:00', 'Osaka'),
        ('GMT+09:00', 'Sapporo'),
        ('GMT+09:00', 'Seoul'),
        ('GMT+09:00', 'Tokyo'),
        ('GMT+09:00', 'Yakutsk'),
        ('GMT+09:30', 'Adelaide'),
        ('GMT+09:30', 'Darwin'),
        ('GMT+10:00', 'Brisbane'),
        ('GMT+10:00', 'Canberra'),
        ('GMT+10:00', 'Guam'),
        ('GMT+10:00', 'Hobart'),
        ('GMT+10:00', 'Melbourne'),
        ('GMT+10:00', 'Port Moresby'),
        ('GMT+10:00', 'Sydney'),
        ('GMT+10:00', 'Vladivostok'),
        ('GMT+11:00', 'Magadan'),
        ('GMT+11:00', 'New Caledonia'),
        ('GMT+11:00', 'Solomon Is.'),
        ('GMT+11:00', 'Srednekolymsk'),
        ('GMT+12:00', 'Auckland'),
        ('GMT+12:00', 'Fiji'),
        ('GMT+12:00', 'Kamchatka'),
        ('GMT+12:00', 'Marshall Is.'),
        ('GMT+12:00', 'Wellington'),
        ('GMT+12:45', 'Chatham Is.'),
        ('GMT+13:00', 'Nuku\'alofa'),
        ('GMT+13:00', 'Samoa'),
        ('GMT+13:00', 'Tokelau Is.'),
    )
    time_zone = models.CharField(max_length=9, choices=TIME_ZONE, default='GMT-08:00')

    # user profile info
    age = models.IntegerField()

    GENDER = (
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
        ('Faʻafafine', 'Faʻafafine'),
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
        ('Man', 'Man'),
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
        ('Trans*', 'Trans*'),
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
        ('Vakasalewalewa', 'Vakasalewalewa'),
        ('Waria', 'Waria'),
        ('Winkte', 'Winkte'),
        ('Woman', 'Woman'),
        ('Woman of trans experience', 'Woman of trans experience'),
        ('X-gender', 'X-gender'),
        ('X-jendā', 'X-jendā'),
        ('Xenogender', 'Xenogender'),
    )
    gender = models.CharField(max_length=50, choices=GENDER)

    PRONOUN_CHOICES = (
        ('They/Them/Theirs', 'They/Them/Theirs'),
        ('He/Him/His', 'He/Him/His'),
        ('She/Her/Hers', 'She/Her/Hers'),
        ('Ze/Hir/Hirs', 'Ze/Hir/Hirs'),
        ('Other', 'Other'),
    )
    personal_pronoun = models.CharField(max_length=50, choices=PRONOUN_CHOICES)

    def __str__(self):
        if self.is_verified:
            return f"{self.user.username} (verified)"
        else:
            return f"{self.user.username} (unverified)"


class AccountBalance(models.Model):
    # link to user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # account balance
    balance = models.FloatField(default=0.0)


class Transaction(models.Model):
    # link to user models
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')

    # link AccountBalance model
    AccountBalance = models.ForeignKey(AccountBalance, on_delete=models.CASCADE)

    # transaction info
    transaction_time = models.DateTimeField(auto_now_add=True)
    transaction_amount = models.FloatField()
    TRANSACTION_TYPE = (
        ('P', 'Pending'),
        ('D', 'Declined'),
        ('C', 'Completed'),
    )
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPE, default='P')
    transaction_description = models.TextField()

    def __str__(self):
        return f'{self.from_user.username} -> {self.to_user.username} {self.transaction_amount}'




