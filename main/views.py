# main/views.py
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from main.forms import ProductForm
from main.models import Product
from django.contrib import messages
from django.contrib.auth import login, logout  # authenticate tidak dipakai
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def show_main(request):
    filter_value = request.GET.get("filter", "all")

    if filter_value == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)

    context = {
        'npm': '2406435231',
        'name': 'Jonathan Yitskhaq Rundjan',
        'class': 'PBP C',
        'product_list': product_list,
        'last_login': request.COOKIES.get('last_login', 'Never'),
    }
    return render(request, "main.html", context)

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
    return HttpResponse(serializers.serialize("json", Product.objects.all()),
                        content_type="application/json")

def show_xml_by_id(request, id):  # <uuid:id> di urls → nama param harus `id`
    obj = get_object_or_404(Product, pk=id)
    return HttpResponse(serializers.serialize("xml", [obj]), content_type="application/xml")

def show_json_by_id(request, id):  # samakan juga di urls.py
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
