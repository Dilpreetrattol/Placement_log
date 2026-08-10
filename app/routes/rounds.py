from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from app import db
from app.models import Round, Application
rounds_bp = Blueprint('rounds', __name__)

@rounds_bp.route('/add/<int:application_id>', methods=['GET', 'POST'])
def add_round(application_id): 
    application = Application.query.get_or_404(application_id)
    if request.method == 'POST':
        round_type = request.form['round_type']
        round_date = request.form.get('round_date')
        performance_rating = request.form.get('performance_rating')
        topics_asked = request.form.get('topics_asked')
        outcome = request.form['outcome']

        new_round = Round(
            application_id=application_id,
            round_type=round_type,
            round_date=datetime.strptime(round_date, '%Y-%m-%d').date() if round_date else None,
            performance_rating=performance_rating,
            topics_asked=topics_asked,
            outcome=outcome
        )
        db.session.add(new_round)
        db.session.commit()
        flash(f'Round added for {application.company.name}.', 'success')
        return redirect(url_for('applications.application_detail', id=application_id))

    return render_template('rounds/add.html', application=application)

@rounds_bp.route('/<int:id>/delete', methods=['POST'])
def delete_round(id):
    round_instance = Round.query.get_or_404(id)
    application_id = round_instance.application_id
    db.session.delete(round_instance)
    db.session.commit()
    flash('Round deleted.', 'info')
    return redirect(url_for('applications.application_detail', id=application_id))

