from django.db import models

def upload_fitness_centre_cover(instance, filename):
    return f'fitness-centre/{instance.id}/{filename}'


class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FitnessCentre(BaseModel):
    owner = models.OneToOneField("accounts.CustomUser", on_delete=models.CASCADE, related_name="fitness_centre")
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
    membership_type = models.ForeignKey(FitnessCentreMembership, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
   
    def __str__(self):
        return f'{self.member} - {self.membership_type}'


    