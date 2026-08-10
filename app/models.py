from . import db
from datetime import datetime

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tier = db.Column(db.String(20), nullable=False)  # FAANG/Product/Service/Startup/PSU
    ctc_min = db.Column(db.Float)
    ctc_max = db.Column(db.Float)
    cgpa_cutoff = db.Column(db.Float)
    bond_years = db.Column(db.Integer, default=0)
    mode = db.Column(db.String(20))  # on-campus / off-campus
    website = db.Column(db.String(200))
    applications = db.relationship('Application', backref='company', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Company {self.name}>'

class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    date_applied = db.Column(db.Date, default=datetime.utcnow)
    current_status = db.Column(db.String(30), default='Applied')
    # Applied/Shortlisted/OA/OA Result/TR1/TR2/HR/Offer/Reject
    why_i_want_this = db.Column(db.Text)
    notes = db.Column(db.Text)
    rounds = db.relationship('Round', backref='application', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Application for {self.company_id}>'

class Round(db.Model):
    __tablename__ = 'rounds'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    round_type = db.Column(db.String(20), nullable=False)  # OA/TR1/TR2/HR
    round_date = db.Column(db.Date)
    performance_rating = db.Column(db.Integer)  # 1-5
    topics_asked = db.Column(db.Text)  # comma-separated, e.g. "DP,Graphs,OS"
    outcome = db.Column(db.String(20))  # Passed/Failed/Pending

    def topics_list(self):
        if self.topics_asked:
            return [t.strip() for t in self.topics_asked.split(',')]
        return []