from timetracker.celery import app
from timetracker.sheets.models import TimeSheet


@app.task
def generate_csv_file_for_timesheet(sheet_id, end_datetime):
    sheet = TimeSheet.objects.get(pk=sheet_id)
    sheet.generate_csv_file()
