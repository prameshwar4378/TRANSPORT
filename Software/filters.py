
from django_filters import FilterSet, ModelChoiceFilter, DateFilter
import django_filters
from django.forms import Select, DateInput
from Developer.models import *



 
class BillFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date'}),
        label='Start Date'
    )
    end_date = django_filters.DateFilter(
        field_name='created_at',
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
    

    def __init__(self, *args, **kwargs):
        super(BillFilter, self).__init__(*args, **kwargs)
        self.filters['start_date'].label = "Start Date"
        self.filters['end_date'].label = "End Date"

    class Meta:
        model = Bill
        fields = ['created_at', 'commission', 'pending_amount', 'from_location', 'to_location', 'reference', 'vehicle', 'driver', 'party', 'bill_number']


