from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import RegisterForm
from .models import Content

# Create your views here.

# @login_required
def index(request):
    contents = Content.objects.all()
    return render(request, 'index.html', {'contents': contents})


def login(request):
    return render(request, 'index/login.html')



def register(request):
    return render(request, 'index/register.html')
