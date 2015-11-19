from StringIO import StringIO
from unicodecsv import writer as csvwriter
from xlsxwriter import Workbook

from flask import send_file

XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


def make_csv_response(rows, basename):
    output = StringIO()
    writer = csvwriter(output)
    if len(rows):
        headers = rows[0].keys()
        writer.writerow(headers)
        for row in rows:
            writer.writerow([row.get(h) for h in headers])
    output.seek(0)
    return send_file(output, mimetype='text/csv', as_attachment=True,
                     attachment_filename='%s.csv' % basename)


def make_xlsx_response(sheets, basename):
    output = StringIO()
    workbook = Workbook(output)
    header_format = workbook.add_format({
        'bold': True,
        'border': 1
    })

    for title, rows in sheets.items():
        if not len(rows):
            continue

        worksheet = workbook.add_worksheet(title)

        row_idx = 0
        headers = None
        for row in rows:
            if headers is None:
                headers = row.keys()
                for c, cell in enumerate(headers):
                    worksheet.write(row_idx, c, cell, header_format)
                row_idx += 1

            col_idx = 0
            for cell in headers:
                worksheet.write(row_idx, col_idx, row.get(cell))
                col_idx += 1
            row_idx += 1

        worksheet.freeze_panes(1, 0)

    workbook.close()
    output.seek(0)
    return send_file(output, mimetype=XLSX_MIME, as_attachment=True,
                     attachment_filename='%s.xlsx' % basename)
