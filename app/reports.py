import json
from app.models import Store, Report
from app.time import compute_uptime
from app.database import db
from datetime import datetime

def generate_report(report_id):
    # Creating new report object and add it to the database
    report = Report(report_id=report_id, status='Running', data='')
    db.session.add(report)
    db.session.commit()

    try:
        # Generating report data
        report_data = []
        stores = Store.query.all()
        for store in stores:
            uptime, downtime = compute_uptime(store.id)
            report_data.append({
                'store_id': store.id,
                'status': store.status,
                'uptime': round(uptime, 2),
                'downtime': round(downtime, 2)
            })

        # Updating report object with status and completed_at
        report.status = 'Complete'
        report.completed_at = datetime.utcnow()

        # Updating report data object with generated report data
        report.data = json.dumps(report_data)

        db.session.commit()

        return report
    except Exception as e:
        # Handle any exceptions and mark the report as failed
        report.status = 'Failed'
        report.completed_at = datetime.utcnow()
        report.data = str(e)
        db.session.commit()
        raise


def get_report_status(report_id):
    report = Report.query.filter_by(report_id=report_id).first()
    if report is None:
        return None
    else:
        return report.status


def get_report_data(report_id):
    report = Report.query.filter_by(report_id=report_id).first()
    if report is None:
        raise ValueError(f"No report found for report_id: {report_id}")
    return report.data
