from django.db import models
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError
# Create your models here.

def validate_letters_only(value):
    if not re.match(r'^[A-Za-z]+$',value):
        raise ValidationError('this field should only contain letter')

class Category(models.Model):
    Id=models.IntegerField(primary_key=True)
    letters_only=RegexValidator(r'^[A-Za-z]+$','only letters are allowed')
    title=models.CharField(max_length=50,unique=True,validators=[validate_letters_only])
    created_at=models.DateTimeField()
    updated_at=models.DateTimeField()
    class Meta:
        verbose_name_plural="categories"