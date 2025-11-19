from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import IntegrityError
import json

@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login successful!"
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login failed, account is disabled."
            }, status=401)
    else:
        return JsonResponse({
            "status": False,
            "message": "Login failed, please check your username or password."
        }, status=401)

@csrf_exempt
def register(request):
    if request.method != 'POST':
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)

    data = {}

    if request.body:
        try:
            if 'application/json' in request.content_type:
                data = json.loads(request.body)
        except (json.JSONDecodeError, TypeError):
            data = {}

    if not data:
        data = request.POST.dict()

    username = data.get('username', '').strip()
    password1 = data.get('password1')
    password2 = data.get('password2')

    if not username or not password1 or not password2:
        return JsonResponse({
            "status": False,
            "message": "All fields are required."
        }, status=400)

    if password1 != password2:
        return JsonResponse({
            "status": False,
            "message": "Passwords do not match."
        }, status=400)
    
    if User.objects.filter(username=username).exists():
        return JsonResponse({
            "status": False,
            "message": "Username already exists."
        }, status=400)
    
    try:
        user = User.objects.create_user(username=username, password=password1)
    except IntegrityError:
        return JsonResponse({
            "status": False,
            "message": "Unable to create user at this time. Please try again."
        }, status=400)
    
    return JsonResponse({
        "username": user.username,
        "status": 'success',
        "message": "User created successfully!"
    }, status=200)

@csrf_exempt
def logout(request):
    username = request.user.username
    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logged out successfully!"
        }, status=200)
    except:
        return JsonResponse({
            "status": False,
            "message": "Logout failed."
        }, status=401)