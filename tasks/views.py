from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse

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
    else:
        print('Obteniendo datos')
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'])
                user.save()
                return HttpResponse('Guardado')            
            except Exception as e:
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

    return render(request, 'signup.html', {
        'form': UserCreationForm
    })

