import csv
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.db.models.options import Options

class ExportAsCSVMixin:
    def export_csv(self, request: HttpRequest, qweryset: QuerySet):
        meta: Options = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filname={meta}-export.csv'

        csv_writer = csv.writer(response)

        csv_writer.writerow(field_names)

        for obj in qweryset:
            csv_writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_csv.short_description = 'Export as CSV'
