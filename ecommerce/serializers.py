from rest_framework import serializers
from ecommerce.models import Category, Subcategory, Product

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategoryDetailSerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True)
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Category
        fields = '__all__'