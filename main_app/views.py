# Add the following import
from django.shortcuts import render, redirect
from .models import Dog
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import VetVisitForm

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def dogs_index(request):
  dogs = Dog.objects.all()  
  return render(request, 'dogs/index.html', { 'dogs': dogs })

def dogs_detail(request, dog_id):
  dog = Dog.objects.get(id=dog_id)
  vetvisit_form = VetVisitForm()
  return render(request, 'dogs/detail.html', { 'dog': dog, 'vetvisit_form' : vetvisit_form })\

def add_vetvisit(request, dog_id):
  form = VetVisitForm(request.POST)
  if form.is_valid():
    new_vetvisit = form.save(commit=False)
    new_vetvisit.dog_id = dog_id
    new_vetvisit.save()
  return redirect('detail', dog_id=dog_id)

class DogCreate(CreateView):
  model = Dog
  fields = '__all__'

class DogUpdate(UpdateView):
  model = Dog
  fields = ['breed', 'description', 'age']

class DogDelete(DeleteView):
  model = Dog
  success_url = '/dogs/'
