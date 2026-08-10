from flask import Blueprint, render_template
from datetime import date
from app.config import config
from app import db
from app.models import Application, Company, Round

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Countdown
    season_start = date(2025, 8, 1)  # Update this via .env in production
    today = date.today()
    days_left = (season_start - today).days

    total_apps = Application.query.count()
    offers = Application.query.filter_by(current_status='Offer').count()

    return render_template('index.html',
                           days_left=days_left,
                           total_apps=total_apps,
                           offers=offers)

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

    return render_template('dashboard.html',
                           status_counts=status_counts,
                           tier_counts=tier_counts,
                           topic_freq=topic_freq_sorted)