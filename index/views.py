from django.contrib.auth import login
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .forms import ContentForm
from django.contrib.auth.decorators import login_required
from .models import HelpContent
from .models import SupportContent
from account.models import UserProfile, AccountBalance
from django.utils import timezone


def index(request):
    if request.user.userprofile.is_active == False:
        return redirect('account_disabled')

    return redirect('index_help')


@login_required(login_url='/account/login/')
def index_help(request):
    if request.user.userprofile.is_active == False:
        return redirect('account_disabled')

    help_contents = HelpContent.objects.filter(is_show=True)

    context = {
        'help_contents': help_contents
    }

    return render(request, 'index/index_help.html', context)


@login_required(login_url='/account/login/')
def index_support(request):
    if request.user.userprofile.is_active == False:
        return redirect('account_disabled')

    support_contents = SupportContent.objects.filter(is_show=True)

    context = {
        'support_contents': support_contents
    }
    return render(request, 'index/index_support.html', context)


@login_required(login_url='/account/login/')
def add_content(request):
    # 检查用户账户是否活跃
    if request.user.userprofile.is_active == False:
        return redirect('account_disabled')

    # 获取用户的个人资料和账户余额
    user_profile = UserProfile.objects.get(user=request.user)
    account_balance, created = AccountBalance.objects.get_or_create(user=request.user)

    # 初始化表单并处理POST请求
    if request.method == 'POST':
        form = ContentForm(request.POST)
        if form.is_valid():
            comment_type = form.cleaned_data['comment_type']
            max_accept_user = form.cleaned_data['max_accept_user']
            total_money = form.cleaned_data['total_money']
            accept_time_limit = form.cleaned_data['accept_time_limit']
            content = form.cleaned_data['content']

            # 确保 accept_time_limit 是 aware datetime
            if accept_time_limit is not None:
                if timezone.is_naive(accept_time_limit):
                    accept_time_limit = timezone.make_aware(accept_time_limit, timezone.get_current_timezone())

            # 根据表单选择创建HelpContent或SupportContent
            if comment_type == 'Help':
                HelpContent.objects.create(
                    push_user=request.user,
                    max_accept_user=max_accept_user,
                    total_money=total_money,
                    accept_time_limit=accept_time_limit,
                    content=content,
                )
                messages.success(request, 'Help content created successfully.')
            else:
                SupportContent.objects.create(
                    push_user=request.user,
                    max_accept_user=max_accept_user,
                    total_money=total_money,
                    accept_time_limit=accept_time_limit,
                    content=content,
                )
                messages.success(request, 'Support content created successfully.')

            return redirect('index')  # 替换为你希望跳转的成功页面
    else:
        form = ContentForm()

    # 传递表单和账户余额等信息到模板
    context = {
        'user_name': request.user.username,
        'account_balance': str(account_balance).split(",")[1],
        'form': form,  # 加入表单到模板上下文
    }
    return render(request, 'add/add_content.html', context)
