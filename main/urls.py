# main/urls.py
from django.urls import path, re_path
from main.views import (
    show_main,
    add_product,
    show_product,
    show_xml,
    show_json,
    show_xml_by_id,
    show_json_by_id,
    register,
    login_user,
    logout_user,
    edit_product,
    delete_product,
)

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('add-product/', add_product, name='add_product'),

    # ==== TERIMA UUID ATAU INT ====
    re_path(
        r'^product/(?P<id>(?:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|\d+))/$',
        show_product,
        name='show_product'
    ),
    re_path(
        r'^product/(?P<id>(?:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|\d+))/edit/$',
        edit_product,
        name='edit_product'
    ),
    re_path(
        r'^product/(?P<id>(?:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|\d+))/delete/$',
        delete_product,
        name='delete_product'
    ),
    # ==== ===================== ====

    # API (biarkan seperti semula jika memang ingin UUID saja)
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<uuid:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<uuid:id>/', show_json_by_id, name='show_json_by_id'),

    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
