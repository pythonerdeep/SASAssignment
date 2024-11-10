import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from store.models import Category, Product, Order

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpass")

@pytest.mark.django_db
def test_create_category(client,user):
    client.force_authenticate(user=user)
    response = client.post('/api/categories/', {"name": "Plant", "description": "Plant"})
    assert response.status_code == 201
    assert response.data['name'] == "Plant"

@pytest.mark.django_db
def test_create_product(client,user):
    client.force_authenticate(user=user)
    category = Category.objects.create(name="Electronics", description="Electronic items")
    response = client.post('/api/products/', {
        "name": "Laptop",
        "description": "A high-performance laptop",
        "price": "1000.00",
        "category": category.id,
        "stock": 10
    })
    assert response.status_code == 201
    assert response.data['name'] == "Laptop"

@pytest.mark.django_db
def test_create_order_insufficient_stock(client, user):
    category = Category.objects.create(name="Electronics", description="Electronic items")
    product = Product.objects.create(name="Laptop", description="A high-performance laptop", price="1000.00", category=category, stock=0)
    client.force_authenticate(user=user)
    
    response = client.post('/api/orders/', {
        "products": [product.id]
    })
    assert response.status_code == 400
    assert "out of stock" in response.data['products'][0]

@pytest.mark.django_db
def test_create_order_success(client, user):
    category = Category.objects.create(name="Electronics", description="Electronic items")
    product = Product.objects.create(name="Laptop", description="A high-performance laptop", price="1000.00", category=category, stock=10)
    client.force_authenticate(user=user)
    
    response = client.post('/api/orders/', {
        "products": [product.id]
    })
    assert response.status_code == 201
    assert response.data['total_amount'] == "1000.00"
