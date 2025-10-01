# main/views.py
import datetime
from uuid import UUID

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import connection  # untuk fallback query ::text (PostgreSQL)

from main.forms import ProductForm
from main.models import Product


# ========= Helper: ambil Product by UUID ATAU INT =========
def _get_product_by_mixed_id(raw_id):
    """
    Mencoba memuat Product dengan id bertipe UUID ATAU INT.
    Urutan:
      1) Coba parse ke UUID -> get(pk=UUID)
      2) Kalau gagal, coba int -> get(pk=int)
      3) Fallback khusus PostgreSQL: WHERE id::text = %s (cover kasus '2' saat kolom UUID)
    """
    s = str(raw_id).strip()

    # 1) Coba sebagai UUID
    try:
        uid = UUID(s)
        return get_object_or_404(Product, pk=uid)
    except (ValueError, TypeError):
        pass

    # 2) Coba sebagai INT
    try:
        i = int(s)
        return get_object_or_404(Product, pk=i)
    except (ValueError, TypeError):
        pass

    # 3) Fallback PostgreSQL: cocokkan string id dengan cast ke text
    #    Menangani kasus saat kolom adalah UUIDField tetapi URL berisi "2" (string),
    #    supaya tidak kena ValidationError saat to_python(UUID).
    table = Product._meta.db_table  # e.g. "main_product"
    try:
        with connection.cursor() as cur:
            cur.execute(f'SELECT id FROM "{table}" WHERE id::text = %s LIMIT 1', [s])
            row = cur.fetchone()
        if row:
            return get_object_or_404(Product, pk=row[0])
    except Exception:
        # kalau bukan PostgreSQL / cast gagal, biarkan lanjut ke 404
        pass

    raise Http404("Product not found")


# ========= API SERIALIZER =========
def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    try:
        obj = _get_product_by_mixed_id(id)
        return HttpResponse(serializers.serialize("xml", [obj]), content_type="application/xml")
    except Http404:
        return HttpResponse(serializers.serialize("xml", []), content_type="application/xml")

def show_json_by_id(request, id):
    try:
        obj = _get_product_by_mixed_id(id)
        return HttpResponse(serializers.serialize("json", [obj]), content_type="application/json")
    except Http404:
        return HttpResponse(serializers.serialize("json", []), content_type="application/json")


# ========= LIST / MAIN =========
def show_products(request):
    products = Product.objects.all()
    return render(request, "main/product_list.html", {"products": products})

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")  # default 'all'

    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)

    context = {
        'npm': '2406435231',
        'name': request.user.username,
        'class': 'PBP C',
        'product_list': product_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }
    return render(request, "main.html", context)


# ========= CRUD =========
def add_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "add_product.html", context)

@login_required(login_url='/login')
def show_product(request, id):
    product = _get_product_by_mixed_id(id)
    context = {'product': product}
    return render(request, "product_detail.html", context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form': form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def edit_product(request, id):
    product = _get_product_by_mixed_id(id)

    if product.user != request.user:
        return redirect('main:show_main')

    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {'form': form, 'product': product}
    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = _get_product_by_mixed_id(id)

    if product.user != request.user:
        messages.error(request, 'You are not allowed to delete this product.')
        return redirect('main:show_main')

    product_name = product.name
    product.delete()
    messages.success(request, f'Product "{product_name}" has been deleted successfully!')
    return HttpResponseRedirect(reverse('main:show_main'))
