def test_index_shows_stats(client, application):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Acme Corp' in resp.data


def test_dashboard_empty_state(client):
    resp = client.get('/dashboard')
    assert resp.status_code == 200
    assert b"there's nothing to chart" in resp.data


def test_dashboard_with_data(client, application):
    resp = client.get('/dashboard')
    assert resp.status_code == 200
    assert b'statusChart' in resp.data


def test_export_csv(client, application):
    resp = client.get('/export/csv')
    assert resp.status_code == 200
    assert resp.headers['Content-Type'].startswith('text/csv')
    assert b'Acme Corp' in resp.data
