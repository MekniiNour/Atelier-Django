from django.db import models
from Categorie.models import Category
from django.core.validators import MaxValueValidator,FileExtensionValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
# Create your models here.
class Conference(models.Model):
    Id=models.IntegerField(primary_key=True)
    title=models.CharField(max_length=200)
    description=models.TextField()
    program=models.FileField(upload_to='files/',validators=[FileExtensionValidator(allowed_extensions=['pdf','png','jpeg','jpg'],message="only pdf,png,jpeg,jpg allowed")])
    capacity=models.IntegerField(validators=[MaxValueValidator(limit_value=900,message="la capacité de la conférence ne dépasse pas un certain nombre maximal.")])
    start_date=models.DateField(default=timezone.now().date())
    end_date=models.DateField()
    location=models.CharField(max_length=15)
    price=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    def clean(self):
        if (self.end_date) <= (self.start_date):
            raise ValidationError('End date must be after start date')
    class Meta:
        constraints=[
            models.CheckConstraint(
                check=models.Q(
                    start_date=timezone.now().date()
                ),
                name="the start date must be greater or equal"
            )
        ]