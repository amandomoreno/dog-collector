from django.db import models
from django.urls import reverse
from datetime import date 
from django.contrib.auth.models import User

VISIT = (
    ('A', 'Adult Vaccines'),
    ('P', 'Puppy Vaccines')
)

class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'pk': self.id})

# Create your models here.
class Dog(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    age = models.IntegerField()
    toys = models.ManyToManyField(Toy)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'dog_id': self.id})

    def visited_for_today(self):
        return self.vetvisit_set.filter(date=date.year()).count() >= len(VISIT)

    class Meta:
        ordering = ['id']

class VetVisit(models.Model):
  date = models.DateField('Vet visit date')
  visit = models.CharField(
      max_length=1,
      choices=VISIT,
    # set the default value for meal to be 'A'
      default=VISIT[0][0]
    )

  # Create a dog_id FK
  dog = models.ForeignKey(Dog, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.get_visit_display()} on {self.date}"

  class Meta:
      ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for dog_id: {self.dog_id} @{self.url}"