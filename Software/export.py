import openpyxl
from django.http import HttpResponse
from django.shortcuts import render
from .filters import *
from openpyxl.styles import Font 
from datetime import date
from .filters import *

from django.utils.timezone import localtime
from django.db.models import Sum, Count, Q, F

def export_filtered_bill_records(request):
    queryset = Bill.objects.all().order_by('id')
    filter = BillFilter(request.GET, queryset=queryset)
    filtered_rec = filter.qs  # Filtered queryset

    # Create a new Workbook and add a sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Bill Report"

    # Define the header row for the Excel sheet
    headers = ['Bill Number', 'Vehicle Number', 'Vehicle Owner', 'Driver', 'Party', 
               'From Location', 'To Location', 'Commission Amount', 'Commission Advance',  'Commission Pending', 
               'Commission Pay Date', 'Bill Date']
    ws.append(headers)

    # Loop through each filtered record and append data to the sheet
    for bill in filtered_rec:
        row = [
            bill.bill_number, 
            bill.vehicle.vehicle_number if bill.vehicle else '',  # Assuming 'vehicle_number' is a field in the 'Vehicle' model
            bill.vehicle.owner.owner_name if bill.vehicle.owner.owner_name else '',  # Assuming 'name' is the field you want from the VehicleOwner model
            bill.driver.driver_name if bill.driver else '',  # Assuming 'name' is the field you want from the Driver model
            bill.party.name if bill.party else '',  # Assuming 'name' is the field you want from the Party model
            bill.from_location,
            bill.to_location,
            bill.commission_charge,
            bill.commission_received,  
            bill.commission_pending,  
            bill.commission_received_date,  # Assuming commission_received_date is the commission pay date
            bill.bill_date,
        ]
        ws.append(row)

    # Create an HTTP response with the Excel file content
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Bill Details.xlsx'

    # Save the workbook to the response
    wb.save(response)

    return response