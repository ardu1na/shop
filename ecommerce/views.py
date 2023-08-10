
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ecommerce.models import Category, Product
from ecommerce.serializers import CategorySerializer, ProductSerializer, CategoryDetailSerializer


## todo
# product detail page





@api_view(['GET'])
def category_detail(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
        serializer = CategoryDetailSerializer(category)
        return Response(serializer.data)
    except Category.DoesNotExist:
        return Response(status=404)



@api_view(['GET'])
def products(request):
    products = Product.objects.all()  # Retrieve all categories from the database
    serializer = ProductSerializer(products, many=True)  # Serialize the queryset

    return Response(serializer.data)  # Return serialized data in the response



@api_view(['GET'])
def categories(request):
    categories = Category.objects.all()  # Retrieve all categories from the database
    serializer = CategorySerializer(categories, many=True)  # Serialize the queryset

    return Response(serializer.data)  # Return serialized data in the response


