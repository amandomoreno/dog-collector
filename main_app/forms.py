from django.forms import ModelForm
from .models import VetVisit

class VetVisitForm(ModelForm):
  class Meta:
    model = VetVisit
    fields = ['date', 'visit']