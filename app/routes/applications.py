from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Application, Company
from datetime import datetime
applications_bp = Blueprint('applications', __name__)

STATUSES = ['Applied', 'Shortlisted', 'OA', 'OA Result', 'TR1', 'TR2', 'HR', 'Offer', 'Reject']

@applications_bp.route('/')
def list_applications():
    applications = Application.query.order_by(Application.date_applied.desc()).all()
    return render_template('applications/list.html', applications=applications)

@applications_bp.route('/add', methods=['GET', 'POST'])
def add_application():
    if request.method == 'POST':
        application = Application(
            company_id=request.form['company_id'],
            current_status=request.form['current_status'],
            date_applied=datetime.strptime(request.form['date_applied'], '%Y-%m-%d').date(),
            notes=request.form.get('notes'),
            why_i_want_this=request.form.get('why_i_want_this')
        )
        db.session.add(application)
        db.session.commit()
        company = Company.query.get(application.company_id)
        flash(f'Application for {company.name} added successfully.', 'success')
        return redirect(url_for('applications.list_applications'))
    return render_template('applications/form.html', companies=Company.query.order_by(Company.name).all(),
                           statuses=STATUSES, application=None)

@applications_bp.route('/<int:id>')
def application_detail(id):
    application = Application.query.get_or_404(id)
    return render_template('applications/detail.html', application=application)

@applications_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_application(id):
    application = Application.query.get_or_404(id)
    if request.method == 'POST':
        application.company_id = request.form['company_id']
        application.current_status = request.form['current_status']
        application.date_applied = datetime.strptime(request.form['date_applied'], '%Y-%m-%d').date()
        application.notes = request.form.get('notes')
        application.why_i_want_this = request.form.get('why_i_want_this')
        db.session.commit()
        flash(f'Application for {application.company.name} updated.', 'success')
        return redirect(url_for('applications.application_detail', id=application.id))
    return render_template('applications/form.html', companies=Company.query.order_by(Company.name).all(),
                           statuses=STATUSES, application=application)

@applications_bp.route('/<int:id>/delete', methods=['POST'])
def delete_application(id):
    application = Application.query.get_or_404(id)
    db.session.delete(application)
    db.session.commit()
    company = Company.query.get(application.company_id)
    flash(f'Application for {company.name} deleted.', 'info')
    return redirect(url_for('applications.list_applications'))
