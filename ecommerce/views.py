
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ecommerce.models import Category, Product, \
    Cart, ProductCart, Client
from ecommerce.serializers import CategorySerializer, ProductSerializer, CategoryDetailSerializer, \
    CartSerializer, CartDetailSerializer, ProductCartSerializer

##########################
################################## Main Products and Categories Display 

""" 
    ## TODO ##
    # product detail page
"""

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

##########################
################################## 





##########################
################################## Cart and shopping logic


## TODO:
# including ammount of product in form or really adding it from product_detail
# deleting cart after certain ammount of time
@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_product_into_cart(request, product_id):
    client = request.user.client
    cart, created = Cart.objects.get_or_create(client=client, done=False)
    try:
        product = Product.objects.get(pk=product_id)
        product_cart, created = ProductCart.objects.get_or_create(cart=cart, product=product)
                
        product_serializer = ProductCartSerializer(instance=product_cart)
        cart_serializer = CartSerializer(instance=cart)

        return Response({'product_cart':product_serializer.data, 'cart':cart_serializer.data}, status=status.HTTP_201_CREATED)
    
    except Product.DoesNotExist:
        return Response(status=404)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_detail(request):
    client = request.user.client
    try:
        cart = Cart.objects.get(client=client, done=False)
        cart_serializer = CartDetailSerializer(instance=cart)
        return Response({'cart':cart_serializer.data}, status=status.HTTP_200_OK)
    
    except Cart.DoesNotExist:
        return Response(status=404)
    


### TODO
# delete cart item
# add quantity into item
# checkout - cart done

