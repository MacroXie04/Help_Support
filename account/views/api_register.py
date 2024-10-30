import json
from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import make_password
from .send_code import sent_verification_code
from account.models import UserProfile
from django.views.decorators.csrf import csrf_protect
import time

# maximum number of email code attempts before locking the account (time in seconds)
CODE_SEND_INTERVAL = 60
VERIFICATION_TIMEOUT = 300


@require_POST
@csrf_protect
def api_register(request):
    data = json.loads(request.body)
    action = data.get('action')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    code = data.get('code')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    gender = data.get('gender')
    phone = data.get('phone')

    # Action to send verification code
    if action == 'send_verification_code' and email:
        return handle_verification_code(email)

    # Action to register a new user
    elif action == 'register' and username and password and code and email and first_name and last_name and gender and phone:
        return handle_registration(username, password, email, code, first_name, last_name, gender, phone)

    # Invalid request
    return JsonResponse({'success': False, 'username': 'Invalid request parameters'}, status=400)


def handle_verification_code(email):
    if User.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'email': 'This email is already registered'}, status=400)

    verification_data = cache.get(f'verification_data_{email}')
    if verification_data:
        last_sent = verification_data.get("timestamp")
        if last_sent and (time.time() - last_sent < CODE_SEND_INTERVAL):
            return JsonResponse({'success': False, 'verification_code': 'You can only request a new code every 60 seconds'},
                                status=429)

    try:
        code = sent_verification_code(email)
        if code:
            cache.set(f'verification_data_{email}', {'code': code, 'timestamp': time.time()},
                      timeout=VERIFICATION_TIMEOUT)
            return JsonResponse({'success': True, 'verification_code': 'Verification code sent'}, status=200)
        else:
            return JsonResponse({'success': False, 'verification_code': 'Failed to send verification code'}, status=500)
    except Exception as e:
        return JsonResponse({'success': False, 'verification_code': 'Failed to send verification code'}, status=500)


# Helper function to handle registration
def handle_registration(username, password, email, code, first_name, last_name, gender, phone):
    # Retrieve and validate the cached verification data
    verification_data = cache.get(f'verification_data_{email}')
    if not verification_data:
        return JsonResponse({'success': False, 'verification_code': 'Verification code expired'}, status=400)

    cached_code = verification_data.get('code')
    if int(cached_code) != int(code):
        return JsonResponse({'success': False, 'verification_code': 'Invalid verification code'}, status=400)

    # Check if email already exists
    if User.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'email': 'This email is already registered'}, status=400)

    # Check if username already exists
    if User.objects.filter(username=username).exists():
        return JsonResponse({'success': False, 'username': 'This username is already taken'}, status=400)

    # Register the new user
    try:
        # Create the user with basic fields
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name
        )

        # Create user profile for additional fields
        UserProfile.objects.create(
            user=user,
            phone=phone,
            gender=gender,
        )

        cache.delete(f'verification_data_{email}')  # Clear the code after successful registration
        return JsonResponse({'success': True, 'message': 'Registration successful', 'redirect_url': '/login/'},
                            status=201)
    except Exception as e:
        return JsonResponse({'success': False, 'verification_code': 'Registration failed'}, status=500)
