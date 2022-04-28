import openpyxl
import pandas

template = r"C:\Users\39528\Documents\bill.xlsx"
newfilename = 'test.xlsx'
wb = openpyxl.Workbook()
ws = wb.active

sheet = openpyxl.load_workbook(template).active
for row in range(1, sheet.max_row + 1):
    line = []
    for col in range(1, sheet.max_column + 1):
        value = sheet.cell(row=row, column=col).value or ''
        line.append(value.replace('{name}', 'dmitry'))
    ws.append(line)

wb.save(newfilename)

excel = pandas.read_excel(newfilename)
excel.to_html('test.html')
