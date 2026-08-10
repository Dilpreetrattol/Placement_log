from app.models import Company


def test_list_companies_empty(client):
    resp = client.get('/companies/')
    assert resp.status_code == 200
    assert b'No companies added yet' in resp.data


def test_add_company(client, app):
    resp = client.post('/companies/add', data={
        'name': 'Globex', 'tier': 'FAANG', 'ctc_min': '30', 'ctc_max': '50',
        'cgpa_cutoff': '8', 'bond_years': '2', 'mode': 'on-campus', 'website': ''
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert Company.query.filter_by(name='Globex').count() == 1


def test_company_detail_404_for_missing(client):
    resp = client.get('/companies/999')
    assert resp.status_code == 404


def test_edit_company(client, company):
    resp = client.post(f'/companies/{company.id}/edit', data={
        'name': 'Acme Corp Renamed', 'tier': 'Product', 'ctc_min': '10', 'ctc_max': '25',
        'cgpa_cutoff': '7', 'bond_years': '1', 'mode': 'on-campus', 'website': ''
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert Company.query.get(company.id).name == 'Acme Corp Renamed'


def test_delete_company_cascades(client, app, company, application):
    from app.models import Application
    resp = client.post(f'/companies/{company.id}/delete', follow_redirects=True)
    assert resp.status_code == 200
    assert Company.query.get(company.id) is None
    assert Application.query.count() == 0
