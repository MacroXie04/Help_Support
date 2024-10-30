from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from account.models import UserProfile
from account.models import AccountBalance
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST


@require_POST
@csrf_protect
@login_required(login_url='/account/login/')
def api_user_info(request):
    # request database
    user_profile = UserProfile.objects.get(user=request.user)

    if not request.user.userprofile.is_active:
        return JsonResponse({'success': False, 'message': 'Account is disabled'}, status=403)

    user_balance = AccountBalance.objects.get(user=request.user)

    context = {
        # base info
        'user_name': request.user.username,
        'user_email': request.user.email,
        'user_full_name': f'{request.user.first_name} {request.user.last_name}',

        # profile info
        'user_phone': user_profile.phone,
        'user_balance': user_balance.balance,
        'user_created_at': user_profile.creatAt,
        'user_gender': user_profile.gender


    }

    return JsonResponse(context)

@require_POST
@csrf_protect
@login_required(login_url='/account/login/')
def user_info_short(request):
    user_balance = AccountBalance.objects.get(user=request.user)

    context = {
        'user_name': request.user.username,
        'user_email': request.user.email,
        'user_balance': user_balance.balance,
    }

    return JsonResponse(context)
