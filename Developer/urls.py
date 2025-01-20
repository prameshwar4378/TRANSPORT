from django.urls import path

from django.conf import settings
from django.conf.urls.static import static 
from .views import *

urlpatterns = [
    path('dashboard/', dashboard, name='developer_dashboard'), 
    
    path('business_list/', business_list, name='developer_business_list'),
    path('create_business/', create_business, name='developer_create_business'),
    path('update_business/<int:id>', update_business, name='developer_update_business'),
    path('delete_business/<int:id>', delete_business, name='developer_delete_business'),

    path('user_list/', user_list, name='developer_user_list'),
    path('create_user/', create_user, name='developer_create_user'),
    path('update_user/<int:id>', update_user, name='developer_update_user'),
    path('delete_user/<int:id>', delete_user, name='developer_delete_user'),
    
]+static(settings.STATIC_URL,document_root=settings.MEDIA_ROOT) 