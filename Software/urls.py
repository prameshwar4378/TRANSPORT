from django.urls import path

from django.conf import settings
from django.conf.urls.static import static 
from .views import *

urlpatterns = [
    path('dashboard/', dashboard, name='software_dashboard'), 

    path('owner_list/', owner_list, name='software_owner_list'),
    path('create_owner/', create_owner, name='software_create_owner'),
    path('update_owner/<int:id>', update_owner, name='software_update_owner'),
    path('delete_owner/<int:id>', delete_owner, name='software_delete_owner'),
    
    path('vehicle_list/', vehicle_list, name='software_vehicle_list'),
    path('create_vehicle/', create_vehicle, name='software_create_vehicle'),
    path('update_vehicle/<int:id>', update_vehicle, name='software_update_vehicle'),
    path('delete_vehicle/<int:id>', delete_vehicle, name='software_delete_vehicle'),

    path('party_list/', party_list, name='software_party_list'),
    path('create_party/', create_party, name='software_create_party'),
    path('update_party/<int:id>', update_party, name='software_update_party'),
    path('delete_party/<int:id>', delete_party, name='software_delete_party'),

    path('driver_list/', driver_list, name='software_driver_list'),
    path('create_driver/', create_driver, name='software_create_driver'),
    path('update_driver/<int:id>', update_driver, name='software_update_driver'),
    path('delete_driver/<int:id>', delete_driver, name='software_delete_driver'),
    
]+static(settings.STATIC_URL,document_root=settings.MEDIA_ROOT) 