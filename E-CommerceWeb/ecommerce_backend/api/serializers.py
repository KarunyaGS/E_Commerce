from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product
import re

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=3)
    confirm_password = serializers.CharField(write_only=True, min_length=3)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True, max_length=30)
    last_name = serializers.CharField(required=True, max_length=30)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def validate_email(self, value):
        """
        Validate email format and domain
        """
        if not value:
            raise serializers.ValidationError("Please provide a valid email address.")
        
        # Check if email contains @
        if '@' not in value:
            raise serializers.ValidationError("Please provide a valid email address.")
        
        # Check for valid email domains
        valid_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'gmail.in', 'yahoo.in']
        email_domain = value.split('@')[-1].lower()
        
        if email_domain not in valid_domains:
            raise serializers.ValidationError("Please use a valid email domain (gmail.com, yahoo.com, etc.)")
        
        # Check if email already exists
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        
        return value

    def validate_password(self, value):
        """
        Validate password requirements
        """
        if len(value) < 3:
            raise serializers.ValidationError("Password must be at least 3 characters long.")
        
        return value

    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("First name is required.")
        return value.strip()

    def validate_last_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Last name is required.")
        return value.strip()

    def validate_username(self, value):
        """
        Validate username requirements
        """
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long.")
        
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        
        return value

    def validate(self, attrs):
        """
        Validate password confirmation
        """
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        # Remove confirm_password from validated_data
        validated_data.pop('confirm_password', None)
        
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']  # Django will handle bcrypt hashing
        )
        return user

class ProductSerializer(serializers.ModelSerializer):
    ct_id = serializers.IntegerField(source="ct.ct_id", read_only=True)
    class Meta:
        model = Product
        fields = ['pdt_id', 'pdt_name', 'pdt_mrp', 'pdt_dis_price', 'pdt_qty', 'ct_id']


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(source='products.count', read_only=True)
    class Meta:
        model = Category
        fields = ['ct_id', 'ct_name', 'ct_description', 'ct_date', 'products_count']
