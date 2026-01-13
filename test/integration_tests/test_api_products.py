import pytest

@pytest.mark.usefixtures("create_default_users", "create_default_products")
class TestProductsApi:

    def test_get_all_products(self, client, tokens):
        response = client.get('/api/v1/products/?limit=50&offset=0', headers={"Authorization": f"Bearer {tokens['access_token']}"})
        result_data = response.json()
        assert response.status_code == 200
        assert len(result_data.get('message')) == 4

    def test_products_by_id(self, client, tokens):
        response = client.get('/api/v1/products/1', headers={"Authorization": f"Bearer {tokens['access_token']}"})
        result_data = response.json()
        assert response.status_code == 200
        assert result_data.get('message').get('id') == 1