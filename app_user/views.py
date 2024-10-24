from django.contrib.auth import get_user_model, authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema

from app_user.models import AppUser
from app_user.serializers import SignUpSerializer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse 


User = get_user_model()

@swagger_auto_schema(method='post', request_body=SignUpSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number')
        address = serializer.validated_data.get('address')
        account_type = serializer.validated_data.get('account_type', 'basic')
        name = serializer.validated_data.get('name')
        gender = serializer.validated_data.get('gender')
        dob = serializer.validated_data.get('dob')
        qualification = serializer.validated_data.get('qualification')
        vcn_number = serializer.validated_data.get('vcn_number')  # New field
        specialization_category = serializer.validated_data.get('specialization_category')  # New field
        university = serializer.validated_data.get('university')  # New field
        state = serializer.validated_data.get('state')  # New field

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            phone_number=phone_number,
            address=address,
            account_type=account_type,
            name=name,
            gender=gender,
            dob=dob,
            qualification=qualification,
            vcn_number=vcn_number,  # New field
            specialization_category=specialization_category,  # New field
            university=university,  # New field
            state=state  # New field
        )
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    department = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'address', 'account_type']



@swagger_auto_schema(method='post', request_body=SignUpSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number')
        address = serializer.validated_data.get('address')
        account_type = serializer.validated_data.get('account_type', 'basic')
        name = serializer.validated_data.get('name')
        gender = serializer.validated_data.get('gender')
        dob = serializer.validated_data.get('dob')
        qualification = serializer.validated_data.get('qualification')
        

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            phone_number=phone_number,
            address=address,
            account_type=account_type,
            name=name,
            gender=gender,
            dob=dob,
            qualification=qualification
        )
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='post', request_body=SignInSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def sign_in(request):
    username = request.data.get('username')
    password = request.data.get('password')
    department = request.data.get('department')
    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password, account_type=department)
    
    
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)
    
    if user.account_type == department:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, "id": user.id}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Unauthorised Department'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_detail(request, user_id):
    try:
        user = AppUser.objects.get(pk=user_id)
    except AppUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AppUserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='get', responses={200: UserSerializer(many=True)})
@api_view(['GET'])
@permission_classes([AllowAny])
def all(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




@swagger_auto_schema(method='put', request_body=UserSerializer, responses={200: UserSerializer()})
@api_view(['PUT'])
@permission_classes([AllowAny])
def update_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(method='delete', responses={204: 'No Content'})
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@swagger_auto_schema(method='get', responses={200: UserSerializer()})
@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_detail(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)



