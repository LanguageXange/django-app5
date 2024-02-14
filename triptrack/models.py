from django.db import models
from django.core.validators import MaxValueValidator
#user auth
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
# trips & notes (images)
class Trip(models.Model):
    city = models.CharField(max_length=50)
    countryCode = models.CharField(max_length=2)
    start_date = models.DateField(blank=True, null=True) #optional
    end_date = models.DateField(blank=True, null=True) #optional 
    # many to one relationship
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "mytrips")


    def __str__(self):
        return self.city
    

class Note (models.Model):
    NOTE_TYPE = (
        ("event", "Event"),
        ("dining", "Dining"),
        ("experience", "Experience"),
        ("general", "General"),
    )
    trip = models.ForeignKey(Trip,on_delete = models.CASCADE, related_name = "mynotes" )
    name = models.CharField(max_length=100)
    desc = models.TextField()
    type = models.CharField(max_length=100, choices=NOTE_TYPE)
    img = models.ImageField(upload_to='notes', blank=True, null=True)
    # pillow
    rating = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(5)]) # 0-5


    def __str__(self):
        return f"{self.name} in {self.trip.city}"