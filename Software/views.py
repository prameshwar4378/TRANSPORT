from django.shortcuts import render,get_object_or_404,redirect
from .forms import *
# Create your views here.
from django.core.exceptions import ValidationError
from django.contrib import messages
from datetime import date
from django.db.models import Sum
from django.http import JsonResponse
from django.db import  transaction
from django.utils.timezone import localdate
from django.db.models import Count
from datetime import datetime, timedelta 
from django.db.models.functions import TruncDate

def dashboard(request): 
    today = localdate()  # Get today's date

    # Filter today's bills
    today_bills = Bill.objects.filter(bill_date=today)

    # Calculate totals
    total_bills_generated = today_bills.count()
    total_commission_amount = today_bills.aggregate(Sum('commission_charge'))['commission_charge__sum'] or 0
    received_commission = today_bills.aggregate(Sum('commission_received'))['commission_received__sum'] or 0
    pending_commission = today_bills.aggregate(Sum('commission_pending'))['commission_pending__sum'] or 0

    total_owners = VehicleOwner.objects.count()
    total_vehicles = Vehicle.objects.count()
    total_parties = Party.objects.count()
    total_drivers = Driver.objects.count()
 
    context = {
        'total_bills_generated': total_bills_generated,
        'total_commission_amount': total_commission_amount,
        'received_commission': received_commission,
        'pending_commission': pending_commission,
        'total_owners': total_owners,
        'total_vehicles': total_vehicles,
        'total_parties': total_parties,
        'total_drivers': total_drivers,
    }

    return render(request, 'software_dashboard.html', context)


def owner_list(request): 
    form=OwnerForm()
    rec=VehicleOwner.objects.select_related().order_by('-id') 
    return render(request, 'software_owner_list.html',{'form':form,'rec':rec} )

def create_owner(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    fm=form.save(commit=False)
                    fm.business = request.user.business
                    fm.save()
                    return JsonResponse({'success': True, 'message': 'Owner created successfully!'})
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

def update_owner(request, id):
    owner = get_object_or_404(VehicleOwner, id=id)  # Safely retrieve the Driver instance or return a 404 error
    if request.method == 'POST':
        form = OwnerForm(request.POST, request.FILES, instance=owner)  # Populate the form with the instance data
        if form.is_valid():
            form.save()  # Save the updated owner inst 
            messages.success(request, 'Owner Updated Successfully.')
        else:
            messages.error(request, 'Form is Not Valid')

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
            if owner_data:
                parts = owner_data.split(' - ') # Split the string into name and phone number
                name, mobile_number = parts
                name = name.strip()
                mobile_number = mobile_number.strip() 
                owner, created = VehicleOwner.objects.get_or_create(owner_name=name,owner_mobile_number=mobile_number) 
            try:
                with transaction.atomic():
                    vehicle = form.save(commit=False)
                    vehicle.business = request.user.business
                    vehicle.owner = owner  # Associate with the existing or new owner
                    vehicle.save() 
                    if not created:
                        messages.success(request, 'Vehicle created successfully with an existing owner!')
                    else:
                        messages.success(request, 'Vehicle created successfully with a new owner!')
                    return JsonResponse({'success': True})
            except ValidationError as e:
                return JsonResponse({'success': False, 'errors': {'non_field_errors': str(e)}}, status=400)
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)}, status=500)
        else:
            errors = {
                field: [str(error) for error in error_list]
                for field, error_list in form.errors.items()
            }
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)



def update_vehicle(request, id): 
    vehicle = get_object_or_404(Vehicle, id=id)  # Safely retrieve the Driver instance or return a 404 error
    if request.method == 'POST':
        form = VehicleUpdateForm(request.POST, request.FILES, instance=vehicle)  # Populate the form with the instance data

        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle Updated Successfully.')
    else:
        form = VehicleUpdateForm(instance=vehicle)  # Populate the form with the existing vehicle data on GET request
    
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

                    messages.success(request, 'Party Created successfully.')
                    return JsonResponse({'success': True})
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


from django.core.paginator import Paginator
from .filters import *

def bill_list(request):
    # Create the form instance

    bill_form = BillForm(initial={'bill_date':date.today()})

    # Optimize Bill Query
    bill_rec = Bill.objects.only(
        'id', 'from_location', 'to_location', 'rent_amount', 'pending_amount'
    ).order_by('-id')
    owner_rec = VehicleOwner.objects.only('id', 'owner_name').order_by('-id')
    vehicle_rec = Vehicle.objects.only('id', 'vehicle_number').order_by('-id')
    party_rec = Party.objects.only('id', 'name', 'mobile').order_by('-id')
    driver_rec = Driver.objects.only('id', 'driver_name', 'mobile').order_by('-id')

    filter = BillFilter(request.GET, queryset=bill_rec)
    filtered_rec = filter.qs  # Filtered queryset
    # Pagination
    paginator = Paginator(filtered_rec, 50)  # Show 10 job cards per page.
    page_number = request.GET.get('page')  # Get the page number from the GET request
    page_obj = paginator.get_page(page_number)  # Get the corresponding page object
    
    # Include the filter parameters in the pagination context
    filter_params = request.GET.copy()  # Copy the GET parameters
    if 'page' in filter_params:
        del filter_params['page']  # Remove the page parameter if it exists
    
    context={
        'bill_form': bill_form, 
        'bill_rec': page_obj,
        'owner_rec': owner_rec,
        'party_rec': party_rec,
        'driver_rec': driver_rec,
        'vehicle_rec': vehicle_rec,
        'filter_params': filter_params.urlencode(),
        'filter': filter,
        }
    return render(
        request,
        'software_bill_list.html',
        context
    )


 
def create_bill(request):
    if request.method == 'POST':
        form = BillForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                name_pattern = r"^[A-Za-z ]+$"
                phone_pattern = r"^\d{10}$"
                
                #Create Vehicle Record
                vehicle_number=request.POST.get('vehicle') 
                vehicle = Vehicle.objects.filter(vehicle_number=vehicle_number).first()
                if not vehicle:
                    vehicle=Vehicle.objects.create(vehicle_number=vehicle_number)
 

                # Create owner Record
                owner = request.POST.get('owner')  
                if owner:
                    try:
                        if '-' in owner:
                            owner = str(owner).strip()
                            parts = owner.split(' - ', 1)
                            name, mobile_number = parts
                            name = name.strip()
                            mobile_number = mobile_number.strip() 
                            # Check or create driver record
                            owner, created = VehicleOwner.objects.get_or_create(owner_name=name, owner_mobile_number=mobile_number)
                            Vehicle.objects.filter(vehicle_number=vehicle_number).update(owner=owner)
                        else:
                            owner = None
                    except Exception as e:
                        # Log the error or handle it as needed
                        print(f"Error while creating or retrieving the owner: {e}")
                        owner = None
                else:
                    owner = None
 
                # Create Driver Record
                driver = request.POST.get('driver')  
                if driver:
                    try:
                        if '-' in driver:
                            driver = str(driver).strip()
                            parts = driver.split(' - ', 1)
                            name, mobile_number = parts
                            name = name.strip()
                            mobile_number = mobile_number.strip() 
                            # Check or create driver record
                            driver, created = Driver.objects.get_or_create(driver_name=name, mobile=mobile_number)
                        else:
                            driver = None
                    except Exception as e:
                        # Log the error or handle it as needed
                        print(f"Error while creating or retrieving the driver: {e}")
                        driver = None
                else:
                    driver = None


                # Create Party Record
                party = request.POST.get('party')  
                if party:
                    try:
                        if '-' in party:
                            party = str(party).strip()
                            parts = party.split(' - ', 1)
                            name, mobile_number = parts
                            name = name.strip()
                            mobile_number = mobile_number.strip() 
                            # Check or create driver record
                            party, created = Party.objects.get_or_create(name=name, mobile=mobile_number)
                        else:
                            party = None
                    except Exception as e:
                        # Log the error or handle it as needed
                        print(f"Error while creating or retrieving the party: {e}")
                        party = None
                else:
                    party = None


                # Create Reference Record
                reference = request.POST.get('reference')  
                if reference:
                    try:
                        if '-' in reference:
                            reference = str(reference).strip()
                            parts = reference.split(' - ', 1)
                            name, mobile_number = parts
                            name = name.strip()
                            mobile_number = mobile_number.strip() 
                            # Check or create driver record
                            reference, created = VehicleOwner.objects.get_or_create(owner_name=name, owner_mobile_number=mobile_number)
                        else:
                            reference = None

                    except Exception as e:
                        # Log the error or handle it as needed
                        print(f"Error while creating or retrieving the reference: {e}")
                        reference = None
                else:
                    reference = None



                with transaction.atomic():
                    fm=form.save(commit=False)
                    fm.business = request.user.business
                    fm.vehicle = vehicle
                    if owner:
                        fm.owner=owner 
                    if driver:
                        fm.driver=driver
                    if party:
                        fm.party=party
                    if party:
                        fm.reference=reference
                    fm.save()
                    messages.success(request, 'Bill created successfully')
                    return JsonResponse({'success': True, 'message': 'Bill created successfully!'})
            except ValidationError as e:
                print(f"Error while creating the bill: {e}")
                return JsonResponse({'success': False, 'errors': {'non_field_errors': str(e)}}, status=400)
            except Exception as e:
                print(f"Error while creating the bill: {e}")
                return JsonResponse({'success': False, 'message': str(e)}, status=500)
        else:
            errors = {
                field: [str(error) for error in error_list]
                for field, error_list in form.errors.items()
            }
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


def get_owner_details(request):
    vehicle_number = request.GET.get('vehicle', '') 
    vehicle=None
    if vehicle_number:
        vehicle = Vehicle.objects.filter(vehicle_number=vehicle_number).first()
        if vehicle:
            name = vehicle.owner.owner_name
            mobile= vehicle.owner.owner_mobile_number
            owner_data=f"{name} - {mobile}" 
 
    if vehicle:
        data = {
            'owner_data': owner_data, 
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Owner not found'})
    

def update_bill(request, id):
    bill = get_object_or_404(Bill, id=id)  # Safely retrieve the Driver instance or return a 404 error
    if request.method == 'POST':
        form = BillUpdateForm(request.POST, request.FILES, instance=bill)  # Populate the form with the instance data
        if form.is_valid():
                form.save()  # Save the updated bill inst 
                messages.success(request, 'Bill Updated Successfully.')
        else:
            errors = {
                field: [str(error) for error in error_list]
                for field, error_list in form.errors.items()
                }
            messages.error(request, f'{errors}') 
    else:
        form = BillUpdateForm(instance=bill)  # Populate the form with the existing bill data on GET request
    return render(request, 'software_update_bill.html', {'form': form,'bill':bill})



def delete_bill(request, id):
    bill = get_object_or_404(Bill, id=id)
    if bill:
        bill.delete()
        messages.success(request, 'Bill deleted successfully.')
    return redirect('/software/bill_list')




def print_bill(request, id):
    bill = get_object_or_404(Bill, id=id) 
    return render(request, 'software_print_bill.html', {'bill':bill})


def get_driver_profile_status(request):
    driver = request.GET.get('driver', '')  # Get 'driver' from the URL parameters
    
    if driver:
        if '-' in driver:
            parts = driver.split(' - ', 1)
            name, mobile_number = parts
            name = name.strip()
            mobile_number = mobile_number.strip()
            
            # Check for the driver record using the name and mobile number
            driver_instance = Driver.objects.filter(driver_name=name, mobile=mobile_number).first()
            
            if driver_instance:
                licence_status = bool(driver_instance.licence)  # True if licence exists, otherwise False
                adhar_card_status = bool(driver_instance.adhar_card)  # True if adhar_card exists, otherwise False
                # Prepare the response data
                data = {
                    'adhar_card': adhar_card_status, 
                    'licence': licence_status,
                }
                return JsonResponse(data)
            else:
                data = {
                    'adhar_card': False, 
                    'licence': False,
                }
                return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Driver data not in proper format (should be "Name - Mobile")'})
    else:
        return JsonResponse({'error': 'Driver data not found'})


def get_party_profile_status(request):
    party = request.GET.get('party', '')  # Get 'party' from the URL parameters
    if party:
        if '-' in party:
            parts = party.split(' - ', 1)
            name, mobile_number = parts
            name = name.strip()
            mobile_number = mobile_number.strip()
            
            # Check for the party record using the name and mobile number
            party_instance = Party.objects.filter(name=name, mobile=mobile_number).first()
 
            if party_instance:
                # Check the status of the specific documents
                adhar_card_status = bool(party_instance.adhar_card)
                pan_card_status = bool(party_instance.pan_card)
                
                # Prepare the response data
                data = {
                    'adhar_card': adhar_card_status, 
                    'pan_card': pan_card_status,
                }
                return JsonResponse(data)
            else:
                # If no party is found, return false for both fields
                data = {
                    'adhar_card': False, 
                    'pan_card': False,
                }
                return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Party data not in proper format (should be "Name - Mobile")'})
    else:
        return JsonResponse({'error': 'Party data not found'})


def get_vehicle_owner_profile_status(request):
    owner = request.GET.get('owner', '')  # Get 'owner' from the URL parameters
    
    if owner:
        if '-' in owner:
            parts = owner.split(' - ', 1)
            name, mobile_number = parts
            name = name.strip()
            mobile_number = mobile_number.strip()
            
            # Check for the vehicle owner record using the name and mobile number
            owner_instance = VehicleOwner.objects.filter(owner_name=name, owner_mobile_number=mobile_number).first()
            
            if owner_instance:
                # Check the status of the specific documents
                adhar_card_status = bool(owner_instance.adhar_card)
                pan_card_status = bool(owner_instance.pan_card)
                
                # Prepare the response data
                data = {
                    'adhar_card': adhar_card_status, 
                    'pan_card': pan_card_status,
                }
                return JsonResponse(data)
            else:
                # If no vehicle owner is found, return false for both fields
                data = {
                    'adhar_card': False, 
                    'pan_card': False,
                }
                return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Owner data not in proper format (should be "Name - Mobile")'})
    else:
        return JsonResponse({'error': 'Owner data not found'})

