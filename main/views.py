# main/views.py
import datetime
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from main.forms import ProductForm
from main.models import Product
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url='/login')
def show_main(request):
    context = {
        'npm': '2406435231',
        'name': 'Jonathan Yitskhaq Rundjan',
        'class': 'PBP C',
        'last_login': request.COOKIES.get('last_login', 'Never'),
    }
    return render(request, "main.html", context)

# AJAX endpoint untuk get products
@login_required(login_url='/login')
def get_products_ajax(request):
    filter_value = request.GET.get("filter", "all")
    
    if filter_value == "all":
        products = Product.objects.all()
    else:
        products = Product.objects.filter(user=request.user)
    
    data = []
    for product in products:
        data.append({
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail or '',
            'category': product.category,
            'category_display': product.get_category_display(),
            'stock': product.stock,
            'is_featured': product.is_featured,
            'is_in_stock': product.is_in_stock,
            'user': product.user.username if product.user else 'Anonymous',
            'is_owner': product.user == request.user if product.user else False,
        })
    
    return JsonResponse({'products': data}, safe=False)

# AJAX endpoint untuk create product
@login_required(login_url='/login')
@csrf_exempt
@require_POST
def create_product_ajax(request):
    try:
        data = json.loads(request.body)
        
        product = Product.objects.create(
            user=request.user,
            name=data.get('name'),
            price=data.get('price', 0),
            description=data.get('description', ''),
            thumbnail=data.get('thumbnail', ''),
            category=data.get('category', ''),
            stock=data.get('stock', 0),
            is_featured=data.get('is_featured', False)
        )
        
        return JsonResponse({
            'status': 'success',
            'message': f'Product "{product.name}" has been created successfully!',
            'product': {
                'id': str(product.id),
                'name': product.name,
                'price': product.price,
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

# AJAX endpoint untuk update product
@login_required(login_url='/login')
@csrf_exempt
@require_POST
def update_product_ajax(request, id):
    try:
        product = get_object_or_404(Product, pk=id)
        
        if product.user != request.user:
            return JsonResponse({
                'status': 'error',
                'message': 'You are not allowed to edit this product.'
            }, status=403)
        
        data = json.loads(request.body)
        
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.description = data.get('description', product.description)
        product.thumbnail = data.get('thumbnail', product.thumbnail)
        product.category = data.get('category', product.category)
        product.stock = data.get('stock', product.stock)
        product.is_featured = data.get('is_featured', product.is_featured)
        product.save()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Product "{product.name}" has been updated successfully!',
            'product': {
                'id': str(product.id),
                'name': product.name,
                'price': product.price,
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

# AJAX endpoint untuk delete product
@login_required(login_url='/login')
@csrf_exempt
@require_POST
def delete_product_ajax(request, id):
    try:
        product = get_object_or_404(Product, pk=id)
        
        if product.user != request.user:
            return JsonResponse({
                'status': 'error',
                'message': 'You are not allowed to delete this product.'
            }, status=403)
        
        name = product.name
        product.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Product "{name}" has been deleted successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

# AJAX endpoint untuk get single product
@login_required(login_url='/login')
def get_product_ajax(request, id):
    try:
        product = get_object_or_404(Product, pk=id)
        
        return JsonResponse({
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail or '',
            'category': product.category,
            'stock': product.stock,
            'is_featured': product.is_featured,
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=404)

# AJAX Login
@csrf_exempt
@require_POST
def login_ajax(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'status': 'success',
                'message': f'Welcome back, {user.username}!',
                'username': user.username,
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid username or password.'
            }, status=401)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

# AJAX Register
@csrf_exempt
@require_POST
def register_ajax(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')
        
        if not username or not password1 or not password2:
            return JsonResponse({
                'status': 'error',
                'message': 'All fields are required.'
            }, status=400)
        
        if password1 != password2:
            return JsonResponse({
                'status': 'error',
                'message': 'Passwords do not match.'
            }, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Username already exists.'
            }, status=400)
        
        if len(password1) < 8:
            return JsonResponse({
                'status': 'error',
                'message': 'Password must be at least 8 characters long.'
            }, status=400)
        
        user = User.objects.create_user(username=username, password=password1)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Your account has been successfully created!',
            'username': user.username,
        }, status=201)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

# AJAX Logout
@csrf_exempt
@require_POST
def logout_ajax(request):
    username = request.user.username
    logout(request)
    return JsonResponse({
        'status': 'success',
        'message': f'Goodbye, {username}! You have been logged out successfully.'
    })

# Keep old views for fallback
@login_required(login_url='/login')
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product_entry = form.save(commit=False)
            product_entry.user = request.user
            product_entry.save()
            messages.success(request, f'Product "{product_entry.name}" has been created successfully!')
            return redirect("main:show_main")
        messages.error(request, 'Failed to create product. Please check the form.')
    else:
        form = ProductForm()
    return render(request, "add_product.html", {"form": form})

@login_required(login_url='/login')
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if product.user != request.user:
        messages.error(request, 'You are not allowed to edit this product.')
        return redirect('main:show_main')

    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        messages.success(request, f'Product "{product.name}" has been updated successfully!')
        return redirect('main:show_main')
    return render(request, "edit_product.html", {'form': form, 'product': product})

@login_required(login_url='/login')
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if product.user != request.user:
        messages.error(request, 'You are not allowed to delete this product.')
        return redirect('main:show_main')
    name = product.name
    product.delete()
    messages.success(request, f'Product "{name}" has been deleted successfully!')
    return HttpResponseRedirect(reverse('main:show_main'))

@login_required(login_url='/login') 
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, "product_detail.html", {'product': product})

def show_xml(request):
    return HttpResponse(serializers.serialize("xml", Product.objects.all()),
                        content_type="application/xml")

def show_json(request):
    products = Product.objects.all()
    data = []
    for product in products:
        data.append({
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'stock': product.stock,
            'is_featured': product.is_featured,
            'user_id': product.user_id,
        })
    return JsonResponse(data, safe=False)

def show_xml_by_id(request, id):
    obj = get_object_or_404(Product, pk=id)
    return HttpResponse(serializers.serialize("xml", [obj]), content_type="application/xml")

def show_json_by_id(request, id):
    obj = get_object_or_404(Product, pk=id)
    return HttpResponse(serializers.serialize("json", [obj]), content_type="application/json")

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            messages.success(request, f'Welcome back, {user.username}!')
            return response
        messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm(request)
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    messages.success(request, 'You have been logged out successfully.')
    return response
