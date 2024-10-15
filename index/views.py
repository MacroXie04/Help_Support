from django.contrib.auth import login
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .forms import HelpContentForm, SupportContentForm
from django.contrib.auth.decorators import login_required
from .models import HelpContent
from .models import SupportContent


def index(request):
    return redirect('index_help')


@login_required(login_url='/account/login/')
def index_help(request):
    help_contents = HelpContent.objects.filter(is_show=True)

    context = {
        'help_contents': help_contents
    }

    return render(request, 'index/index_help.html', context)


@login_required(login_url='/account/login/')
def index_support(request):
    support_contents = SupportContent.objects.filter(is_show=True)

    context = {
        'support_contents': support_contents
    }
    return render(request, 'index/index_support.html', context)


@login_required(login_url='/account/login/')
def add_content(request):
    return render(request, 'add/add_content.html')

