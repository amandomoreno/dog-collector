from django.contrib import admin

# Register your models here.
from .models import Dog, VetVisit

# Register your models here
admin.site.register(Dog)
admin.site.register(VetVisit)
