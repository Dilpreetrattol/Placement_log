from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Application, Company
from datetime import datetime
applications_bp = Blueprint('applications', __name__)

@applications_bp.route('/')
def list_applications():
    applications = Application.query.order_by(Application.date_applied).all()
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
    return render_template('applications/add.html', companies=Company.query.all())

@applications_bp.route('/<int:id>')
def application_detail(id):
    application = Application.query.get_or_404(id)
    return render_template('applications/detail.html', application=application)

@applications_bp.route('/<int:id>/delete', methods=['POST'])
def delete_application(id):
    application = Application.query.get_or_404(id)
    db.session.delete(application)
    db.session.commit()
    company = Company.query.get(application.company_id)
    flash(f'Application for {company.name} deleted.', 'info')
    return redirect(url_for('applications.list_applications'))