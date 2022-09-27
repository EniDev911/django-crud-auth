from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm

# Create your views here.

# la vista que se devolvera al visitar ('/')
def home(request):
    return render(request, 'home.html')

# la vista que se devolverá al visitar ('/signup/')
def signup(request):

    # cuando la petición viene por get se quiere mostrar la interfaz o vista al usuario
    # cuando la petición viene por post se quiere procesar los datos
    if request.method == 'GET':
        print('Enviando formulario')
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        print('Obteniendo datos')
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')     
            except IntegrityError as e:
                print(e)
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'usuario ya existe'
                })
            # la respuesta que se envía cuando se a guardado el usuario
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Contraseña no coinciden'
        })

# la vista que se devolvera al estar autenticado
def tasks(request):
    return render(request, 'tasks.html')

# la vista que se devolverá al crear una nueva tarea
def create_task(request):
    return render(request, 'create_task.html', {
        'form': TaskForm
    })

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):

    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, 
                username=request.POST['username'], 
                password=request.POST['password'])
        if user is None:
             return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'Usuario o password es incorrecto'
        })
        else:
            login(request, user)
            return redirect('tasks')
 