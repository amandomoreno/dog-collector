# Add the following import
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Dog, Toy, Photo
from .forms import VetVisitForm
import uuid
import boto3
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'amandosdogcollector'

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def dogs_index(request):
  dogs = Dog.objects.filter(user=request.user)
  return render(request, 'dogs/index.html', { 'dogs': dogs })

@login_required
def dogs_detail(request, dog_id):
  dog = Dog.objects.get(id=dog_id)
  toys_dog_doesnt_have = Toy.objects.exclude(id__in = dog.toys.all().values_list('id'))
  vetvisit_form = VetVisitForm()
  return render(request, 'dogs/detail.html', { 'dog': dog, 'vetvisit_form' : vetvisit_form, 'toys': toys_dog_doesnt_have })

@login_required
def add_vetvisit(request, dog_id):
  form = VetVisitForm(request.POST)
  if form.is_valid():
    new_vetvisit = form.save(commit=False)
    new_vetvisit.dog_id = dog_id
    new_vetvisit.save()
  return redirect('detail', dog_id=dog_id)

class DogCreate(LoginRequiredMixin, CreateView):
  model = Dog
  fields = ['name', 'breed', 'description', 'age']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class DogUpdate(LoginRequiredMixin, UpdateView):
  model = Dog
  fields = ['breed', 'description', 'age']

class DogDelete(LoginRequiredMixin, DeleteView):
  model = Dog
  success_url = '/dogs/'

class ToyList(LoginRequiredMixin, ListView):
  model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'

@login_required
def assoc_toy(request, dog_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Dog.objects.get(id=dog_id).toys.add(toy_id)
  return redirect('detail', dog_id=dog_id)

@login_required
def add_photo(request, dog_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, dog_id=dog_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', dog_id=dog_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)