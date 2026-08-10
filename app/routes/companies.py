from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Company

companies_bp = Blueprint('companies', __name__)

TIERS = ['FAANG', 'Product', 'Service', 'Startup', 'PSU']

@companies_bp.route('/')
def list_companies():
    companies = Company.query.order_by(Company.tier).all()
    return render_template('companies/list.html', companies=companies)

@companies_bp.route('/add', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        company = Company(
            name=request.form['name'],
            tier=request.form['tier'],
            ctc_min=float(request.form.get('ctc_min') or 0),
            ctc_max=float(request.form.get('ctc_max') or 0),
            cgpa_cutoff=float(request.form.get('cgpa_cutoff') or 0),
            bond_years=int(request.form.get('bond_years') or 0),
            mode=request.form.get('mode'),
            website=request.form.get('website')
        )
        db.session.add(company)
        db.session.commit()
        flash(f'{company.name} added successfully.', 'success')
        return redirect(url_for('companies.list_companies'))
    return render_template('companies/add.html', tiers=TIERS)

@companies_bp.route('/<int:id>')
def company_detail(id):
    company = Company.query.get_or_404(id)
    return render_template('companies/detail.html', company=company)

@companies_bp.route('/<int:id>/delete', methods=['POST'])
def delete_company(id):
    company = Company.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    flash(f'{company.name} deleted.', 'info')
    return redirect(url_for('companies.list_companies'))