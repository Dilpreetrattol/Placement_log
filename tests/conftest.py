import pytest

from app import create_app, db as _db
from app.models import Company, Application, Round


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def company(app):
    c = Company(name='Acme Corp', tier='Product', ctc_min=10, ctc_max=20,
                cgpa_cutoff=7.0, bond_years=1, mode='on-campus', website='https://acme.example')
    _db.session.add(c)
    _db.session.commit()
    return c


@pytest.fixture
def application(app, company):
    from datetime import date
    a = Application(company_id=company.id, current_status='Applied',
                     date_applied=date(2026, 8, 1), why_i_want_this='Great team')
    _db.session.add(a)
    _db.session.commit()
    return a
