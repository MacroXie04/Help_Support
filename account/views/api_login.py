import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.core.cache import cache
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import get_user_model

User = get_user_model()

# maximum number of login attempts before locking the account (time in seconds)
MAX_ATTEMPTS = 5
LOCKOUT_TIME = 300


@csrf_protect
@require_POST
def api_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        identifier = data.get('username')
        password = data.get('password')

        if identifier and password:
            # cache keys
            attempt_cache_key = f'login_attempts_{identifier}'
            lockout_cache_key = f'lockout_{identifier}'

            # check if account is locked
            if cache.get(lockout_cache_key):
                return JsonResponse({
                    'success': False,
                    'error': 'Account locked due to multiple failed attempts. Try again later.'
                }, status=403)

            # give email login priority
            if "@" in identifier:
                try:
                    user = User.objects.get(email=identifier)
                    username = user.username
                except User.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': 'Invalid email. Please try again.'
                    }, status=400)
            else:
                username = identifier

            # authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # reset attempts
                cache.delete(attempt_cache_key)
                login(request, user)
                return JsonResponse({'success': True, 'message': 'Login successful'}, status=200)
            else:
                # increment login attempts
                attempts = cache.get(attempt_cache_key, 0) + 1
                cache.set(attempt_cache_key, attempts, LOCKOUT_TIME)

                if attempts >= MAX_ATTEMPTS:
                    # lock account
                    cache.set(lockout_cache_key, True, LOCKOUT_TIME)
                    return JsonResponse({
                        'success': False,
                        'error': 'Too many failed attempts. Account locked for a while.'
                    }, status=403)
                else:
                    return JsonResponse({
                        'success': False,
                        'error': f'Invalid credentials. Attempt {attempts}/{MAX_ATTEMPTS}'
                    }, status=400)

        return JsonResponse({'success': False, 'error': 'Username or email and password required'}, status=400)

    return JsonResponse({'success': False, 'error': 'Only POST requests are allowed'}, status=405)
