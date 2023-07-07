import secrets
from flask import Blueprint, jsonify, request, Response
from app.reports import generate_report, get_report_status, get_report_data
from app.services import run_import_data

blueprint_report = Blueprint('blueprint_report', __name__, url_prefix='/api')

# Required API endpoint 1: Trigger report generation
@blueprint_report.route('/trigger_report', methods=['POST'])
def trigger_report():
    try:
        report_id = secrets.token_urlsafe(16)
        report = generate_report(report_id)
        return jsonify({'report_id': report.report_id, 'message': 'Report generation triggered', 'status': report.status})
    except Exception as e:
        return jsonify({'error': 'Failed to trigger report generation', 'message': str(e)}), 500


# Required API endpoint 2: Get report in csv format
@blueprint_report.route('/get_report', methods=['GET'])
def get_report():
    try:
        report_id = request.args.get('report_id')
        if not report_id:
            return jsonify({'error': 'Missing report ID'}), 400

        report_status = get_report_status(report_id)
        if not report_status:
            return jsonify({'error': 'Invalid report ID'}), 400

        if report_status == 'Running':
            return jsonify({'status': 'Running', 'message': 'Report is still in progress'})
        elif report_status == 'Complete':
            report_data = get_report_data(report_id)
            if report_data:
                return Response(report_data, mimetype='text/csv')
            else:
                return jsonify({'error': 'Failed to retrieve report data'}), 400
        else:
            return jsonify({'error': 'Invalid report status'}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve report', 'message': str(e)}), 500


# Extra API endpoint 3: To import data from csv to database
@blueprint_report.route('/import_data', methods=['GET'])
def import_data():
    try:
        run_import_data()
        return jsonify({'msg':'Data Successfully imported'})
    except Exception as e:
        return jsonify({'error': 'Failed to import', 'message': str(e)})