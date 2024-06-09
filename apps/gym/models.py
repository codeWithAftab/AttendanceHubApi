from typing import Iterable
from django.db import models
from django.utils import timezone
from helper.id_generator import *
from datetime import timedelta
from datetime import date


def upload_fitness_centre_cover(instance, filename):
    return f'fitness-centre/{instance.id}/{filename}'

class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class FitnessCentre(BaseModel):
    id = models.CharField(max_length=122, default=generate_fitness_centre_id, primary_key=True)
    owner = models.OneToOneField("accounts.CustomUser", on_delete=models.CASCADE, related_name="admin_of_fitness_centre")
    cover_image = models.ImageField(upload_to=upload_fitness_centre_cover, null=True, blank=True)
    name = models.CharField(max_length=123)
    address = models.CharField(max_length=234)
    phone_number = models.CharField(max_length=12)
    zip_code = models.CharField(max_length=12, null=True)
    joined_members = models.ManyToManyField("accounts.CustomUser", null=True, blank=True, related_name="joined_fitness_centres")
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name} | {self.phone_number}"


class FitnessCentreMembership(BaseModel):
    id = models.CharField(max_length=122, default=generate_membership_id, primary_key=True)
    fitness_centre = models.ForeignKey(FitnessCentre, on_delete=models.CASCADE, related_name="memberships")
    title = models.CharField(max_length=122)
    membership_type = models.CharField(max_length=50, choices=[
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual')
    ])
    price = models.IntegerField()
    
    def __str__(self):
        return f'{self.fitness_centre} - {self.membership_type}'


class Membership(BaseModel):
    member = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE )
    # fitness_centre = models.ForeignKey(FitnessCentre, on_delete=models.CASCADE, related_name="sold_memberships")
    membership_type = models.ForeignKey(FitnessCentreMembership, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.datetime.today())
    end_date = models.DateField(null=True)
   
    def __str__(self):
        return f'{self.member} - {self.membership_type}'

    @property
    def is_active(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date

    def set_expiry_date(self):
        membership_type = self.membership_type.membership_type

        if membership_type == "monthly":
            # For monthly membership, expiry date is set to one month after start date
            self.end_date = self.start_date + timedelta(days=30)

        elif membership_type == "annual":
            # For annual membership, expiry date is set to one year after start date
            self.end_date = self.start_date + timedelta(days=365)

        else:
            self.end_date = self.start_date + timedelta(days=90)
        

    def save(self, *args, **kwargs) -> None:
        if not self.end_date:
            self.set_expiry_date()

        super(Membership, self).save(*args, **kwargs)