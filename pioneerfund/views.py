from django.shortcuts import render
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

# from .forms import UserLoginForm, UserRegisterForm

# Create your views here.

def index(request):
    return render(request, 'pioneerfund/index.html')
#

