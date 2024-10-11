from django.db import models
from django.contrib.auth.models import AbstractUser
from Conference.models import Conference
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
# Create your models here.

def email_validator(value):
    if not value.endswith('@esprit.tn'):
        raise ValidationError('this field should end with @esprit.tn')

class Participant(AbstractUser):
    cin_validator=RegexValidator(
        regex=r'\d{8}$',
        message="this field must contain exactly 8 digits"
    )
    cin = models.CharField(max_length=8, primary_key=True,validators=[cin_validator])
    participant_catgory = models.CharField(max_length=10, choices= [
    ('etudiant', 'Etudiant'),
    ('enseignant', 'Enseignant'),
    ('doctorant', 'Doctorant'),
    ('chercheur', 'Chercheur')])
    email = models.EmailField(unique=True,validators=[email_validator])
    username = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    USERNAME_FIELD = 'username'
    Reservation=models.ManyToManyField(Conference,through='Reservation',related_name='Reservation')

class Reservation(models.Model):
    reservation_date=models.DateField(auto_now_add=True)
    confirmed=models.BooleanField(default=False)
    conference=models.ForeignKey(Conference,on_delete=models.CASCADE)
    participant=models.ForeignKey(Participant,on_delete=models.CASCADE)
    def clean(self):
        if self.conference.start_date < timezone.now().date():
            raise ValidationError('you can only reserve for upcoming dates')
        reservation_counts=Reservation.objects.filter(
            participant=self.participant,
            reservation_date=self.reservation_date
        )
        if reservation_counts>=3:
            raise ValidationError('You can only make up to 3 reservations per day')
    class meta:
        unique_together = ('participant', 'conference')

    