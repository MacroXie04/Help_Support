from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect


@login_required(login_url='/account/login/')
def index(request):
    pass

def content(request, content_id):
    pass

@login_required(login_url='/account/login/')
def add_content(request):
    pass