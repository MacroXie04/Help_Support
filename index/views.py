from django.contrib.auth import login
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .forms import HelpContentForm, SupportContentForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='/account/login/')
def index(request):
    return redirect(index_help)


@login_required(login_url='/account/login/')
def index_help(request):
    pass


@login_required(login_url='/account/login/')
def index_support(request):
    pass


@login_required(login_url='/account/login/')
def add_help_content(request):
    if not request.user.is_active:
        return redirect('account_disabled')

    if request.method == 'POST':
        form = HelpContentForm(request.POST)
        if form.is_valid():
            help_content = form.save(commit=False)
            help_content.user = request.user
            help_content.save()
            messages.success(request, "Help content added successfully.")
            return redirect('help_content_list')
    else:
        form = HelpContentForm()
    return render(request, 'add_help_content.html', {'form': form})


@login_required(login_url='/account/login/')
def add_support_content(request):
    if not request.user.is_active:
        return redirect('account_disabled')

    if request.method == 'POST':
        form = SupportContentForm(request.POST)
        if form.is_valid():
            support_content = form.save(commit=False)
            support_content.user = request.user
            support_content.save()
            messages.success(request, "支持内容已成功添加。")
            return redirect('support_content_list')
    else:
        form = SupportContentForm()
    return render(request, 'add_support_content.html', {'form': form})
