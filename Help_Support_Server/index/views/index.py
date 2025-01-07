from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.middleware.csrf import get_token
from index.models import Content
from account.models import UserProfile


@login_required
@api_view(['POST'])
def csrf_token(request):
    # user must be authenticated
    if request.user.userprofile.is_verified == False:
        return JsonResponse({'error': 'User is not verified.'}, status=400)

    # return csrf token
    token = get_token(request)
    return JsonResponse({'csrf_token': token})


@login_required
@api_view(['POST'])
def request_content(request):
    # user must be authenticated
    if request.user.userprofile.is_verified == False:
        return JsonResponse({'error': 'User is not verified.'}, status=400)

    screening_condition = request


    return JsonResponse({'content': 'This is a help content.'})
