from rest_framework import serializers
from ecommerce.models import Category



class CategorySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Category
        fields = '__all__'