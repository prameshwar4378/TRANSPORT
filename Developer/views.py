from django.shortcuts import render,redirect,get_object_or_404
# Create your views here.
from django.contrib.auth import authenticate, login as auth_login, logout as DeleteSession
from django.contrib import messages
from django.contrib.auth.models import User
from . forms import * 
from django.db import  transaction
from django.http import JsonResponse

def index(request):
    return render(request,"index.html")


def login(request): 
    if request.user.is_authenticated:
        return redirect_user_based_on_role(request, request.user)

    if request.method == 'POST': 
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect_user_based_on_role(request, user)
        else:
            messages.error(request, 'Oops...! User does not exist. Please try again.')

    return render(request, 'login.html')



def update_password(request, id):
    user = get_object_or_404(User, id=id)  # Retrieve the Business instance safely
    if request.method == 'POST':
        form = UpdatePasswordForm(request.POST)
        if form.is_valid():
            # Set the new password for the user and save
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password updated successfully.')
    else:
        form = UpdatePasswordForm()
    return render(request, 'developer__update_password.html', {'form': form, 'user': user})


def redirect_user_based_on_role(request, user):
    if user.is_superuser:
        return redirect('/developer/dashboard')
    elif user.is_business:
        return redirect('/software/dashboard') 
    else:
        messages.error(request, 'Unauthorized user role.')
        return redirect('/login')

def logout(request):
    DeleteSession(request) 
    return redirect('/login')



def dashboard(request): 
    return render(request, 'developer_dashboard.html')
 


def business_list(request): 
    form=BusinessForm()
    rec=Business.objects.select_related().order_by('-id')
    return render(request, 'developer_business_list.html',{'form':form,'rec':rec} )

def create_business(request):
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
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

def update_business(request, id):
    business = get_object_or_404(Business, id=id)  # Safely retrieve the Business instance or return a 404 error
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES, instance=business)  # Populate the form with the instance data
        if form.is_valid():
            form.save()  # Save the updated business inst 
            messages.success(request, 'Business Updated Successfully.')
    else:
        form = BusinessForm(instance=business)  # Populate the form with the existing business data on GET request
    
    return render(request, 'developer_update_business.html', {'form': form,'business':business})


def delete_business(request, id):
    business = get_object_or_404(Business, id=id)
    if business:
        business.delete()
        messages.success(request, 'Business deleted successfully.')
    return redirect('/developer/business_list')





def user_list(request): 
    form=CustomUserForm()
    rec=CustomUser.objects.select_related('business').order_by('-id')
    return render(request, 'developer_user_list.html',{'form':form,'rec':rec} )

def create_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    return JsonResponse({'success': True, 'message': 'User created successfully!'})
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

def update_user(request, id):
    user = get_object_or_404(CustomUser, id=id)  # Safely retrieve the CustomUser instance or return a 404 error
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=user)  # Populate the form with the instance data
        if form.is_valid():
            form.save()  # Save the updated user inst 
            messages.success(request, 'User Updated Successfully.')
    else:
        form = CustomUserForm(instance=user)  # Populate the form with the existing user data on GET request
    
    return render(request, 'developer_update_user.html', {'form': form,'user':user})


def delete_user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    if user:
        user.delete()
        messages.success(request, 'User deleted successfully.')
    return redirect('/developer/user_list')
