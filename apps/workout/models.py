from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    class Meta:
        abstract = True

def upload_bodypart_icon(instance, filename):
    return f'excercises/bodyparts/{instance.name}/{filename}'

def upload_excercise_icon(instance, filename):
    return f'excercises//{instance.name}/{filename}'


class BodyPart(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="")
    TYPES = [
        ("upper", "Upper Body Part"),
        ("lower", "Lower Body Part"),
    ]
    body_part_type = models.CharField(choices=TYPES, max_length=12)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    body_parts = models.ManyToManyField(BodyPart, blank=True)
    explaination = models.TextField()

    def __str__(self):
        return self.name