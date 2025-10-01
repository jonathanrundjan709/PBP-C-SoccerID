# main/views.py
import datetime
import uuid

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404

from main.forms import ProductForm
from main.models import Product


def _uuid_or_404(id_str: str) -> uuid.UUID:
    """Validasi id string → UUID atau 404 (tanpa meledak ValidationError)."""
    try:
        return uuid.UUID(str(id_str))
    except (ValueError, AttributeError, TypeError):
        raise Http404("Product not found")


@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")
    base_qs = Product.objects.all() if filter_type == "all" else Product.objects.filter(user=request.user)

    # (Opsional tapi direkomendasikan) tampilkan hanya item dengan pk UUID valid,
    # supaya tidak ada link menuju /product/1/ yang pasti 404.
    valid_ids = []
    for pk in base_qs.values_list('pk', flat=True):
        try:
            uuid.UUID(str(pk))
            valid_ids.append(pk)
        except ValueError:
            # lewati item legacy/non-UUID
            continue

    product_list = base_qs.filter(pk__in=valid_ids)

    context = {
        'npm': '2406435231',
        'name': request.user.username,
        'class': 'PBP C',
        'product_list': product_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }
    return render(request, "main.html", context)


def add_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')
    return render(request, "add_product.html", {'form': form})


@login_required(login_url='/login')
def show_product(request, id):
    pk = _uuid_or_404(id)  # ← bikin 404 ramah kalau id bukan UUID
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {'product': product})


def edit_product(request, id):
    pk = _uuid_or_404(id)
    product = get_object_or_404(Product, pk=pk)

    if product.user != request.user:
        return redirect('main:show_main')

    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    return render(request, "edit_product.html", {'form': form, 'product': product})


def delete_product(request, id):
    pk = _uuid_or_404(id)
    product = get_object_or_404(Product, pk=pk)
    # if product.user != request.user:
    #     return redirect('main:show_main')
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))


def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


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
            return response
    else:
        form = AuthenticationForm(request)
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response
