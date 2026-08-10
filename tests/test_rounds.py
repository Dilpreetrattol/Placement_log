from app.models import Round


def test_add_round(client, application):
    resp = client.post(f'/rounds/add/{application.id}', data={
        'round_type': 'OA', 'round_date': '2026-08-05', 'performance_rating': '4',
        'topics_asked': 'DP, Graphs', 'outcome': 'Passed'
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert Round.query.count() == 1
    assert Round.query.first().performance_rating == 4


def test_add_round_without_rating_stores_none(client, application):
    resp = client.post(f'/rounds/add/{application.id}', data={
        'round_type': 'HR', 'round_date': '', 'performance_rating': '',
        'topics_asked': '', 'outcome': 'Pending'
    }, follow_redirects=True)
    assert resp.status_code == 200
    r = Round.query.first()
    assert r.performance_rating is None
    assert r.round_date is None


def test_delete_round(client, application):
    r = Round(application_id=application.id, round_type='OA', outcome='Passed')
    from app import db
    db.session.add(r)
    db.session.commit()

    resp = client.post(f'/rounds/{r.id}/delete', follow_redirects=True)
    assert resp.status_code == 200
    assert Round.query.count() == 0
