import django_filters
from app.product.models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category', lookup_expr='exact')
    model = django_filters.CharFilter(field_name='model', lookup_expr='exact')

    is_active = django_filters.BooleanFilter(field_name='is_active', lookup_expr='exact')
    is_favorite = django_filters.BooleanFilter(field_name='is_favorite', lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'category', 'model', 'is_active', 'is_favorite']