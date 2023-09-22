from rest_framework import  viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from ecommerce.models import Category, Product, \
    Cart, ProductCart,\
    Client, Location

from ecommerce.serializers import \
    CategorySerializer, ProductSerializer, CategoryDetailSerializer, \
    CartSerializer, CartDetailSerializer, ProductCartSerializer,\
    ClientProfileSerializer, LocationSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def cart_detail(self, request):
        client = self.request.user.client
        try:
            cart = Cart.objects.get(client=client, done=False)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(client=client, done=False)
        serializer = CartDetailSerializer(instance=cart)
        return Response({'cart': serializer.data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add_product_into_cart(self, request, pk=None):
        client = self.request.user.client
        cart, created = Cart.objects.get_or_create(client=client, done=False)
        try:
            product = Product.objects.get(pk=pk)
            product_cart, created = ProductCart.objects.get_or_create(cart=cart, product=product)
            product_serializer = ProductCartSerializer(instance=product_cart)
            cart_serializer = CartSerializer(instance=cart)
            return Response({'product_cart': product_serializer.data, 'cart': cart_serializer.data}, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['delete'])
    def delete_product_from_cart(self, request, pk=None):
        client = self.request.user.client
        try:
            product_cart = ProductCart.objects.get(pk=pk)
            cart = product_cart.cart
            if cart.client == client:
                product_cart.delete()
                cart_serializer = CartSerializer(instance=cart)
                return Response({'cart': cart_serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except ProductCart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
