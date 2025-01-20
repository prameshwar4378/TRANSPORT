from django.shortcuts import render,get_object_or_404,redirect
from .forms import *
# Create your views here.
from django.core.exceptions import ValidationError
from django.contrib import messages


from django.http import JsonResponse
from django.db import  transaction


def dashboard(request): 
    return render(request, 'software_dashboard.html')



def owner_list(request): 
    form=OwnerForm()
    rec=VehicleOwner.objects.select_related().order_by('-id') 
    return render(request, 'software_owner_list.html',{'form':form,'rec':rec} )

def create_owner(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                print(request.user.business.id)
                with transaction.atomic():
                    fm=form.save(commit=True)
                    fm.business=request.user.business
                    fm.save()
                    return JsonResponse({'success': True, 'message': 'Owner created successfully!'})
            except ValidationError as e:
                # Handle explicit model-level validation errors
                print(e)
                return JsonResponse({'success': False, 'errors': {'non_field_errors': str(e)}}, status=400)
            except Exception as e:
                # Catch any unexpected errors and return a 500 response
                print(e)
                return JsonResponse({'success': False, 'message': str(e)}, status=500)
        else:
            # Handle form errors
            errors = {
                field: [str(error) for error in error_list]
                for field, error_list in form.errors.items()
            }
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    
    # If the request method is not POST, return a method not allowed response
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

def update_owner(request, id):
    owner = get_object_or_404(VehicleOwner, id=id)  # Safely retrieve the Driver instance or return a 404 error
    if request.method == 'POST':
        form = OwnerForm(request.POST, request.FILES, instance=owner)  # Populate the form with the instance data
        if form.is_valid():
            form.save()  # Save the updated owner inst 
            messages.success(request, 'Owner Updated Successfully.')
    else:
        form = OwnerForm(instance=owner)  # Populate the form with the existing owner data on GET request
    
    return render(request, 'software_update_owner.html', {'form': form,'owner':owner})


def delete_owner(request, id):
    owner = get_object_or_404(VehicleOwner, id=id)
    if owner:
        owner.delete()
        messages.success(request, 'Owner deleted successfully.')
    return redirect('/software/owner_list')



def vehicle_list(request): 
    form=VehicleForm()
    rec=Vehicle.objects.select_related().order_by('-id')
    owner=VehicleOwner.objects.all()
    return render(request, 'software_vehicle_list.html',{'form':form,'rec':rec,'owner':owner} )

import re
def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            owner_data = request.POST.get("owner")  # Format: "owner name - 7776824564"
            if '-' not in owner_data:
                record_count=VehicleOwner.objects.filter(owner_name=owner_data).count()
                if record_count > 1 :
                    return JsonResponse({'success': False, 'errors': {'non_field_errors': 'Multiple owners with the same name found. try to add mobile number as well'}}, status=400)
                
                owner, created = VehicleOwner.objects.get_or_create(
                        owner_name=owner_data,
                        defaults={
                            'owner_alternate_mobile_number': None,  # Set defaults as needed
                        }
                    )
            else:
                owner_name, owner_mobile = [x.strip() for x in owner_data.split('-')]
                owner, created = VehicleOwner.objects.get_or_create(
                        owner_name=owner_name,
                        owner_mobile_number=owner_mobile,
                        defaults={
                            'owner_alternate_mobile_number': None,  # Set defaults as needed
                        }
                    )
            try:
                
 
                with transaction.atomic():
                    # Check if the owner already exists


                    # Save the vehicle with the retrieved or newly created owner
                    vehicle = form.save(commit=False)
                    vehicle.business = request.user.business
                    vehicle.owner = owner  # Associate with the existing or new owner
                    vehicle.save()

                    message = (
                        'Vehicle created successfully with a new owner!'
                        if created
                        else 'Vehicle created successfully with an existing owner!'
                    )

                    return JsonResponse({'success': True, 'message': message})
            except ValidationError as e:
                # Handle explicit model-level validation errors
                return JsonResponse({'success': False, 'errors': {'non_field_errors': str(e)}}, status=400)
            except Exception as e:
                # Catch any unexpected errors and return a 500 response
                return JsonResponse({'success': False, 'message': str(e)}, status=500)
        else:
            # Handle form errors
            errors = {
                field: [str(error) for error in error_list]
                for field, error_list in form.errors.items()
            }
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    
    # If the request method is not POST, return a method not allowed response
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)



def update_vehicle(request, id): 
    vehicle = get_object_or_404(Vehicle, id=id)  # Safely retrieve the Driver instance or return a 404 error
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)  # Populate the form with the instance data

        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle Updated Successfully.')
    else:
        form = VehicleForm(instance=vehicle)  # Populate the form with the existing vehicle data on GET request
    
    return render(request, 'software_update_vehicle.html', {'form': form,'vehicle':vehicle})


def delete_vehicle(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)
    if vehicle:
        vehicle.delete()
        messages.success(request, 'Vehicle deleted successfully.')
    return redirect('/software/vehicle_list')






def party_list(request): 
    form=PartyForm()
    rec=Party.objects.select_related().order_by('-id')
    return render(request, 'software_party_list.html',{'form':form,'rec':rec} )

def create_party(request):
    if request.method == 'POST':
        form = PartyForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    fm=form.save(commit=True)
                    fm.business=request.user.business 
                    fm.save()
                    return JsonResponse({'success': True, 'message': 'Business created successfully!'})
            except ValidationError as e:
                # Handle explicit model-level validation errors
                return JsonResponse({'success': False, 'errors': {'non_field_errors': str(e)}}, status=400)
            except Exception as e:
                # Catch any unexpected errors and return a 500 response
                return JsonResponse({'success': False, 'message': str(e)}, status=500)
        else:
            # Handle form errors
            errors = {
                field: [str(error) for error in error_list]
                for field, error_list in form.errors.items()
            }
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    
    # If the request method is not POST, return a method not allowed response
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

def update_party(request, id):
    party = get_object_or_404(Party, id=id)  # Safely retrieve the Driver instance or return a 404 error
    if request.method == 'POST':
        form = PartyForm(request.POST, request.FILES, instance=party)  # Populate the form with the instance data
        if form.is_valid():
            form.save()  # Save the updated party inst 
            messages.success(request, 'Party Updated Successfully.')
    else:
        form = PartyForm(instance=party)  # Populate the form with the existing party data on GET request
    
    return render(request, 'software_update_party.html', {'form': form,'party':party})


def delete_party(request, id):
    party = get_object_or_404(Party, id=id)
    if party:
        party.delete()
        messages.success(request, 'Party deleted successfully.')
    return redirect('/software/party_list')






def driver_list(request): 
    form=DriverForm()
    rec=Driver.objects.select_related().order_by('-id')
    return render(request, 'software_driver_list.html',{'form':form,'rec':rec} )

def create_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    fm=form.save(commit=True)
                    fm.business=request.user.business 
                    fm.save()
                    return JsonResponse({'success': True, 'message': 'Business created successfully!'})
            except ValidationError as e:
                # Handle explicit model-level validation errors
                return JsonResponse({'success': False, 'errors': {'non_field_errors': str(e)}}, status=400)
            except Exception as e:
                # Catch any unexpected errors and return a 500 response
                return JsonResponse({'success': False, 'message': str(e)}, status=500)
        else:
            # Handle form errors
            errors = {
                field: [str(error) for error in error_list]
                for field, error_list in form.errors.items()
            }
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    
    # If the request method is not POST, return a method not allowed response
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

def update_driver(request, id):
    driver = get_object_or_404(Driver, id=id)  # Safely retrieve the Driver instance or return a 404 error
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES, instance=driver)  # Populate the form with the instance data
        if form.is_valid():
            form.save()  # Save the updated driver inst 
            messages.success(request, 'Driver Updated Successfully.')
    else:
        form = DriverForm(instance=driver)  # Populate the form with the existing driver data on GET request
    
    return render(request, 'software_update_driver.html', {'form': form,'driver':driver})


def delete_driver(request, id):
    driver = get_object_or_404(Driver, id=id)
    if driver:
        driver.delete()
        messages.success(request, 'Driver deleted successfully.')
    return redirect('/software/driver_list')
