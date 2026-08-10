from app.models import Round


def test_topics_list_splits_and_strips():
    r = Round(round_type='OA', topics_asked='DP, Graphs ,  OS')
    assert r.topics_list() == ['DP', 'Graphs', 'OS']


def test_topics_list_empty_when_none():
    r = Round(round_type='OA', topics_asked=None)
    assert r.topics_list() == []


def test_company_cascade_deletes_applications(app, company, application):
    from app import db
    from app.models import Application

    assert Application.query.count() == 1
    db.session.delete(company)
    db.session.commit()
    assert Application.query.count() == 0
