import openpyxl
from xlsx2html import xlsx2html

from Baumanagement.models.models_contracts import Bill


def tmp(request):
    template = r"C:\Users\WestfaliaBPE\PycharmProjects\Baumanagement\Baumanagement\print_forms\bill.xlsx"
    newfilename = 'test.xlsx'

    obj = Bill.objects.get(id=1)
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

    xlsx2html(newfilename, 'test.html')