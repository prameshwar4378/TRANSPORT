
from django_filters import FilterSet, ModelChoiceFilter, DateFilter
import django_filters
from django.forms import Select, DateInput
from Developer.models import *



 
class BillFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='bill_date',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date'}),
        label='Start Date'
    )
    end_date = django_filters.DateFilter(
        field_name='bill_date',
        lookup_expr='lte',
        widget=DateInput(attrs={'type': 'date'}),
        label='End Date'
    )
    commission_less_than = django_filters.NumberFilter(
        field_name='commission',
        lookup_expr='lte',
        label='Commision  Less Than'
    )
    
    commission_greater_than = django_filters.NumberFilter(
        field_name='commission',
        lookup_expr='gte',
        label='Commision  Greater Than'
    )
    
    commission_less_than = django_filters.NumberFilter(
        field_name='commission_pending',
        lookup_expr='lte',
        label='Commision Pending LTE <='
    )
    
    commission_greater_than = django_filters.NumberFilter(
        field_name='commission_pending',
        lookup_expr='gte',
        label='Commision Pending GTE >= '
    )
    vehicle_owner = django_filters.ModelChoiceFilter(
        queryset=VehicleOwner.objects.all(),  # Get all VehicleOwner records
        field_name='vehicle__owner',  # Link this to the 'Vehicle' model's owner foreign key
        empty_label="---------",  # Default empty label
        label='Vehicle Owner'
    )    
    def __init__(self, *args, **kwargs):
        super(BillFilter, self).__init__(*args, **kwargs)
        self.filters['start_date'].label = "Start Date"
        self.filters['end_date'].label = "End Date"

    class Meta:
        model = Bill
        fields = ['commission_pending',  'from_location', 'to_location', 'reference', 'vehicle', 'driver', 'party', 'bill_number', 'vehicle__owner']


 
