from rest_framework import serializers
from app_user.models import *
from cases.models import Case  # Import Case model
from cases.serializers import CaseSerializer 

###################




###############

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False, max_length=15)
    address = serializers.CharField(required=False)
    account_type = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    dob = serializers.CharField(required=False)
    qualification = serializers.CharField(required=False)
    vcn_number = serializers.CharField(required=False)  # New field
    specialization_category = serializers.CharField(required=False)  # New field
    university = serializers.CharField(required=False)  # New field
    state = serializers.CharField(required=False)  # New field

class AppUserSerializer(serializers.ModelSerializer):
    cases = serializers.SerializerMethodField()  # Add a field to list all cases

    class Meta:
        model = AppUser
        fields = ['id', 'username', 'email', 'phone_number', 'address', 'account_type', 'cases']

    def get_cases(self, obj):
        """
        This method retrieves all cases associated with the user.
        """
        user_cases = Case.objects.filter(app_user=obj)  # Get cases for the user
        return CaseSerializer(user_cases, many=True).data  # Serialize the cases
