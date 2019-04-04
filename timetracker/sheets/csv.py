import csv


def generate_timesheet_csv(buffer_object, sheet, activities):
    fieldnames = [
        'project',
        'activity',
        'duration',
        'start_datetime',
        'end_datetime',
        'description',
    ]
    writer = csv.DictWriter(buffer_object, fieldnames=fieldnames)
    writer.writeheader()

    for activity in activities:
        writer.writerow({
            'project': str(activity.project),
            'activity': activity.activity,
            'duration': activity.duration,
            'start_datetime': activity.start_datetime,
            'end_datetime': activity.end_datetime,
        })
