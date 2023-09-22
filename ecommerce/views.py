
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ecommerce.models import Client, Location
    
from ecommerce.serializers import ClientProfileSerializer, LocationSerializer





##########################
################################## 

### CLIENT

# create or change location
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_client_location(request):
    client = request.user.client
    location, created = Location.objects.get_or_create(client=client)
    
    serializer = LocationSerializer(data=request.data, instance=location)
    if serializer.is_valid():
        location.address = serializer.validated_data['address']
        location.address_number = serializer.validated_data['address_number']
        location.apartament = serializer.validated_data['apartament']
        location.country = serializer.validated_data['country']
        location.state = serializer.validated_data['state']
        location.city = serializer.validated_data['city']
        location.post_code = serializer.validated_data['post_code']

        location.save()
        return Response({'data':serializer.data}, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)
        return Response(status=404)
    
    
    

# see profile 
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



# TODO: ADD CHANGE USER.EMAIL IN THIS USER.CLIENT
# update profile 
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_client_profile(request):
    
    try:
        client = request.user.client
        serializer = ClientProfileSerializer(data=request.data, instance=client)
        if serializer.is_valid():
            client.name = serializer.validated_data['name']
            client.lastname = serializer.validated_data['lastname']
            client.phone = serializer.validated_data['phone']
            client.save()
            return Response({'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
        else:
            print(serializer.errors)
            return Response(status=404)
    
    except Client.DoesNotExist:
        return Response(status=404)