from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import *


class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
  category_id = serializers.IntegerField(write_only=True)
  category = CategorySerializer(read_only=True)

  class Meta:
    model = MenuItem
    fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["id", "last_login", "is_superuser", "username", "first_name", "last_name",
              "email", "is_staff", "is_active", "date_joined", "groups", "user_permissions"]


class CartSerializer(serializers.ModelSerializer):
  menu_item_id = serializers.IntegerField(write_only=True)
  menu_item = MenuItemSerializer(read_only=True)
  user = serializers.PrimaryKeyRelatedField(
      queryset=User.objects.all(),
      default=serializers.CurrentUserDefault()
    )

  class Meta:
    model = Cart
    fields = ['id', 'menu_item_id', 'menu_item', 'user', 'quantity', 'total']


class ItemOrderSerializer(serializers.ModelSerializer):
  menu_item = MenuItemSerializer()

  class Meta:
    model = ItemOrder
    fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
  order = ItemOrderSerializer(many=True)

  class Meta:
    model = Order
    fields = "__all__"
