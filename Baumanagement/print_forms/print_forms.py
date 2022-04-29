import openpyxl
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from xlsx2html import xlsx2html

from Baumanagement.models.models_contracts import Bill


def tmp(request, id):
    template = r"Baumanagement/print_forms/bill.xlsx"
    newfilename = 'tmp/test.xlsx'

    obj = get_object_or_404(Bill, id=id)
    company = obj.contract.company
    replace_dict = {
        'sender': f'{obj.contract.project.company.name} {obj.contract.project.company.address} {obj.contract.project.company.city}',
        'contact': company.contacts.first(),
        'company': company.name,
        'address1': company.address,
        'address2': company.city,
        'bill_number': obj.name,
        'date': obj.date,
    }

    def fill_fields(cell):
        for key, value in replace_dict.items():
            if key:
                cell = cell.replace('{' + key + '}', value or '')
        return cell.strip()

    wb = openpyxl.load_workbook(template)
    sheet = wb.active
    for row in range(1, sheet.max_row + 1):
        for col in range(1, sheet.max_column + 1):
            if sheet.cell(row=row, column=col).value:
                sheet.cell(row=row, column=col).value = fill_fields(sheet.cell(row=row, column=col).value)

    wb.save(newfilename)

    xlsx2html(newfilename, 'tmp/test.html')
    with open('tmp/test.html', 'r') as file:
        html = file.read()

    return HttpResponse(html)
