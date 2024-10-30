from .forms import UserRegisterForm, UserLoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from .models import UserProfile, AccountBalance
from .forms import PaymentForm
from decimal import Decimal



@login_required(login_url='/account/login')
def account_page(request):
    user_profile = UserProfile.objects.get(user=request.user)
    account_balance, created = AccountBalance.objects.get_or_create(user=request.user)
    context = {
        'user_profile': user_profile,
        'user_name': request.user.username,
        'account_balance': str(account_balance).split(",")[1],
    }
    return render(request, template_name='account_page/account_page.html', context=context)

@login_required(login_url='/account/login/')
def add_balance(request):
    if request.user.userprofile.is_active == False:
        return redirect('account_disabled')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            expiration_date = form.cleaned_data['expiration_date']
            security_code = form.cleaned_data['security_code']
            amount = form.cleaned_data['amount']

            print(f'Card Number: {card_number}')
            print(f'Expiration Date: {expiration_date}')
            print(f'Security Code: {security_code}')

            # TODO Process payment information with with bank API

            # Update the account balance
            account_balance = AccountBalance.objects.get(user=request.user)
            account_balance.balance = Decimal(account_balance.balance) + Decimal(amount)
            account_balance.save()

            messages.success(request, f'Payment of ${amount} was successful.')

            return redirect('account_page')

        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = PaymentForm()

    account_balance = AccountBalance.objects.get(user=request.user)
    user_name = request.user.username
    context = {
        'account_balance': str(account_balance).split(",")[1],
        'user_name': user_name,
        'form': form,
    }

    return render(request, template_name='account_page/templates/balance_page/add_balance.html', context=context)

