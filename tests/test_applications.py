from app.models import Application


def test_add_application(client, company):
    resp = client.post('/applications/add', data={
        'company_id': str(company.id), 'current_status': 'Applied',
        'date_applied': '2026-08-01', 'why_i_want_this': 'Interesting work', 'notes': ''
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert Application.query.count() == 1


def test_application_detail(client, application):
    resp = client.get(f'/applications/{application.id}')
    assert resp.status_code == 200
    assert b'Acme Corp' in resp.data


def test_edit_application_status(client, application):
    resp = client.post(f'/applications/{application.id}/edit', data={
        'company_id': str(application.company_id), 'current_status': 'Offer',
        'date_applied': '2026-08-01', 'why_i_want_this': 'Interesting work', 'notes': ''
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert Application.query.get(application.id).current_status == 'Offer'


def test_delete_application(client, application):
    resp = client.post(f'/applications/{application.id}/delete', follow_redirects=True)
    assert resp.status_code == 200
    assert Application.query.count() == 0
