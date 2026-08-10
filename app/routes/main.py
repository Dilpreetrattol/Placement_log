from flask import Blueprint, render_template, current_app
from datetime import date, datetime

from app import db
from app.models import Application, Company, Round

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Countdown, driven by PLACEMENT_SEASON_START in .env / config
    season_start = datetime.strptime(
        current_app.config['PLACEMENT_SEASON_START'], '%Y-%m-%d'
    ).date()
    today = date.today()
    days_left = (season_start - today).days

    total_apps = Application.query.count()
    offers = Application.query.filter_by(current_status='Offer').count()
    active = Application.query.filter(
        Application.current_status.notin_(['Offer', 'Reject'])
    ).count()
    total_companies = Company.query.count()

    recent_applications = Application.query.order_by(
        Application.date_applied.desc()
    ).limit(5).all()

    return render_template('index.html',
                           days_left=days_left,
                           season_start=season_start,
                           total_apps=total_apps,
                           offers=offers,
                           active=active,
                           total_companies=total_companies,
                           recent_applications=recent_applications)

@main_bp.route('/dashboard')
def dashboard():
    # --- Insight queries ---

    # 1. Status breakdown (for pie/bar chart)
    from sqlalchemy import func
    status_counts = db.session.query(
        Application.current_status,
        func.count(Application.id)
    ).group_by(Application.current_status).all()

    # 2. Tier-wise application count
    tier_counts = db.session.query(
        Company.tier,
        func.count(Application.id)
    ).join(Application, Company.id == Application.company_id)\
     .group_by(Company.tier).all()

    # 3. Topic frequency across all rounds
    all_rounds = Round.query.all()
    topic_freq = {}
    for r in all_rounds:
        for topic in r.topics_list():
            if topic:
                topic_freq[topic] = topic_freq.get(topic, 0) + 1
    topic_freq_sorted = sorted(topic_freq.items(), key=lambda x: x[1], reverse=True)[:10]

    # 4. Round outcome breakdown (Passed/Failed/Pending) — conversion funnel
    outcome_counts = db.session.query(
        Round.outcome,
        func.count(Round.id)
    ).group_by(Round.outcome).all()

    # 5. Average performance rating per round type
    rating_by_round = db.session.query(
        Round.round_type,
        func.avg(Round.performance_rating)
    ).filter(Round.performance_rating.isnot(None))\
     .group_by(Round.round_type).all()

    has_data = Application.query.count() > 0

    return render_template('dashboard.html',
                           status_labels=[s for s, _ in status_counts],
                           status_values=[c for _, c in status_counts],
                           tier_labels=[t for t, _ in tier_counts],
                           tier_values=[c for _, c in tier_counts],
                           topic_labels=[t for t, _ in topic_freq_sorted],
                           topic_values=[c for _, c in topic_freq_sorted],
                           outcome_labels=[o or 'Unknown' for o, _ in outcome_counts],
                           outcome_values=[c for _, c in outcome_counts],
                           rating_labels=[r for r, _ in rating_by_round],
                           rating_values=[round(v, 2) for _, v in rating_by_round],
                           has_data=has_data)