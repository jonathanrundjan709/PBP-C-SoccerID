from django.urls import path
from main.views import (
    show_main,
    add_product,
    show_product,
    show_xml, show_json, show_json_by_id, show_xml_by_id,
    register, login_user, logout_user, 
    edit_product, delete_product,
    # AJAX endpoints
    get_products_ajax,
    create_product_ajax,
    update_product_ajax,
    delete_product_ajax,
    get_product_ajax,
    login_ajax,
    register_ajax,
    logout_ajax
)

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),

    # Old endpoints (fallback)
    path('add-product/', add_product, name='add_product'),
    path('product/<uuid:id>/edit/', edit_product, name='edit_product'),
    path('product/<uuid:id>/delete/', delete_product, name='delete_product'),
    path('product/<uuid:id>/', show_product, name='show_product'),

    # AJAX Product endpoints
    path('api/products/', get_products_ajax, name='get_products_ajax'),
    path('api/products/create/', create_product_ajax, name='create_product_ajax'),
    path('api/products/<uuid:id>/', get_product_ajax, name='get_product_ajax'),
    path('api/products/<uuid:id>/update/', update_product_ajax, name='update_product_ajax'),
    path('api/products/<uuid:id>/delete/', delete_product_ajax, name='delete_product_ajax'),

    # AJAX Auth endpoints
    path('api/auth/login/', login_ajax, name='login_ajax'),
    path('api/auth/register/', register_ajax, name='register_ajax'),
    path('api/auth/logout/', logout_ajax, name='logout_ajax'),

    # Serialization
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<uuid:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<uuid:id>/', show_json_by_id, name='show_json_by_id'),

    # Auth pages
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]