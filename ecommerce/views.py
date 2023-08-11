
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ecommerce.models import Category, Product, \
    Cart, ProductCart,\
    Client
from ecommerce.serializers import \
    CategorySerializer, ProductSerializer, CategoryDetailSerializer, \
    CartSerializer, CartDetailSerializer, ProductCartSerializer,\
    ClientProfileSerializer

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

### CLIENT

# profile 
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def client_profile(request):
    
    try:
        client = request.user.client
    
        serializer = ClientProfileSerializer(instance=client)
        return Response(serializer.data)
    except Client.DoesNotExist:
        return Response(status=404)




# profile 
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_client_profile(request):
    
    try:
        client = request.user.client
        serializer = ClientProfileSerializer(data=request.data, instance=client)
        if serializer.is_valid():
            print(serializer)
            client.name = serializer.validated_data['name']
            client.lastname = serializer.validated_data['lastname']
            client.phone = serializer.validated_data['phone']
            client.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(status=404)
    
    except Client.DoesNotExist:
        return Response(status=404)



##########################
################################## Cart and shopping logic
## TODO: not let add a product into cart if not logged in, redirect to login page

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



@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_product_from_cart(request, product_id):
    client = request.user.client
    try:
       # Delete the product from the cart
        try:
            product_cart = ProductCart.objects.get(pk=product_id)
            cart = product_cart.cart
            if cart.client == client:
                product_cart.delete()
        except ProductCart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        cart_serializer = CartSerializer(instance=cart)
        return Response({'cart': cart_serializer.data}, status=status.HTTP_200_OK)
    
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)




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
# link to productdetail in cart for each item
# checkout - cart done

