import csv
import io
from flask import Blueprint, make_response
from app.models import Application, Company

export_bp = Blueprint('export', __name__)

@export_bp.route('/csv')
def export_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Company', 'Tier', 'CTC Range', 'Status', 'Date Applied', 'Notes'])

    apps = Application.query.join(Company).all()
    for app in apps:
        writer.writerow([
            app.company.name,
            app.company.tier,
            f"{app.company.ctc_min}–{app.company.ctc_max} LPA",
            app.current_status,
            app.date_applied,
            app.notes or ''
        ])

    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=placement_log.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response