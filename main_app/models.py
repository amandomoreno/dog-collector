from django.db import models
from django.urls import reverse

VISIT = (
    ('A', 'Adult Vaccines'),
    ('P', 'Puppy Vaccines')
)


# Create your models here.
class Dog(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'dog_id': self.id})

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