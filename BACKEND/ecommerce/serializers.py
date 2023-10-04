from rest_framework import serializers
from ecommerce.models import \
        Category, Subcategory, Product,\
        Cart, ProductCart,\
        Client



##########################
################################## Main Products and Categories Display 

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    subcategory_name = serializers.ReadOnlyField(source='subcategory.name')

    class Meta:
        model = Product
        fields = '__all__'
        #fields = ['id','name','description','price','image','available','category_name', 'subcategory_name']

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
        

##########################
################################## Cart and shopping logic

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class ProductCartSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_id = serializers.ReadOnlyField(source='product.id')
    image = serializers.ImageField(source='product.image')

    class Meta:
        model = ProductCart
        fields = '__all__'


class CartDetailSerializer(serializers.ModelSerializer):
    products = ProductCartSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'
        
        

##########################
################################## Client data

class ClientSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Client
        fields = '__all__'
        

class ClientProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = Client
        fields = ['name','lastname','email','phone', 'address']