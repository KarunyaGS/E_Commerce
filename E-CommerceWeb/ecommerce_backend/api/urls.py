from django.urls import path
from . import views
from .views import RegisterView, search_products, bulk_create_products, CustomTokenObtainPairView, elasticsearch_fulltext_search
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Authentication endpoints (JWT)
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', views.get_user_profile, name='user_profile'),
    
    # Category endpoints
    path('categories/', views.CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:id>/', views.CategoryDetailAPIView.as_view(), name='category-detail'),
    
    # Product endpoints
    path('products/', views.ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:id>/', views.ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/category/<int:id>/', views.ProductListAPIView.as_view(), name='products-by-category'),
    
    # Search endpoints
    path('search/', search_products, name='search_products'),
    path('search/basic/', search_products, name='basic_search'),
    path('search/full/', search_products, name='full_search'),
    path('elasticsearch-search/', elasticsearch_fulltext_search, name='elasticsearch_fulltext_search'),
    
    # Utility endpoints
    path('products/bulk_create/', bulk_create_products, name='bulk_create_products'),
]