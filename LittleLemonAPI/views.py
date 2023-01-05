from django.conf import settings
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import *
from .serializers import *
from .permissions import *
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# TODO: JWT


class CategoryView(viewsets.ModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  permission_classes = [IsAuthenticated]
  search_fields = ['title']

  def get_permissions(self):
    permission_classes = [IsAuthenticated]
    if self.request.method != 'GET':
      permission_classes.append(IsManagerPermission)

    return [permission() for permission in permission_classes]

  @method_decorator(cache_page(settings.DEFAULT_CACHE_TIMEOUT))
  def list(self, request, *args, **kwargs):
    return super().list(request, *args, **kwargs)


class MenuItemView(viewsets.ModelViewSet):
  queryset = MenuItem.objects.all()
  serializer_class = MenuItemSerializer
  permission_classes = [IsAuthenticated]
  ordering_fields = ['price']
  search_fields = ['title']
  filterset_fields = ['category', 'price']

  def get_permissions(self):
    permission_classes = [IsAuthenticated]
    if self.request.method != 'GET':
      permission_classes.append(IsManagerPermission)

    return [permission() for permission in permission_classes]

  @method_decorator(cache_page(settings.DEFAULT_CACHE_TIMEOUT))
  def list(self, request, *args, **kwargs):
    return super().list(request, *args, **kwargs)


class ManagerView(viewsets.ModelViewSet):
  queryset = User.objects.all().filter(groups__name='Manager')
  serializer_class = UserSerializer
  permission_classes = [IsAuthenticated, IsManagerPermission]

  def create(self, request):
    managers = Group.objects.get(name='Manager')
    user = get_object_or_404(User, username=request.POST.get('username'))
    managers.user_set.add(user.pk)
    return Response(status=status.HTTP_201_CREATED)

  def destroy(self, request, pk=None):
    managers = Group.objects.get(name='Manager')
    user = get_object_or_404(User, pk=pk)
    managers.user_set.remove(user.pk)
    return Response(status=status.HTTP_204_NO_CONTENT)


class DeliveryCrewView(viewsets.ModelViewSet):
  queryset = User.objects.all().filter(groups__name='DeliveryCrew')
  serializer_class = UserSerializer
  permission_classes = [IsAuthenticated, IsManagerPermission]

  def create(self, request):
    delivery_crew = Group.objects.get(name='DeliveryCrew')
    user = get_object_or_404(User, username=request.POST.get('username'))
    delivery_crew.user_set.add(user.pk)
    return Response(status=status.HTTP_201_CREATED)

  def destroy(self, request, pk=None):
    delivery_crew = Group.objects.get(name='DeliveryCrew')
    user = get_object_or_404(User, pk=pk)
    delivery_crew.user_set.remove(user.pk)
    return Response(status=status.HTTP_204_NO_CONTENT)


class CartView(viewsets.ModelViewSet):
  queryset = Cart.objects.all()
  serializer_class = CartSerializer
  permission_classes = [IsAuthenticated, IsCustomerPermission]

  def get_queryset(self):
    cart = Cart.objects.all().filter(user=self.request.user)
    return cart

  def destroy(self, request):
    menu_item = get_object_or_404(MenuItem, pk=request.POST.get('menu_item_id'))
    Cart.objects.filter(user=request.user, menu_item=menu_item).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class OrderView(viewsets.ModelViewSet):
  queryset = Order.objects.all()
  serializer_class = OrderSerializer
  permission_classes = [IsAuthenticated, OrderPermission]
  ordering_fields = ['status']

  def get_queryset(self):
    user = self.request.user
    orders = Order.objects.all()

    if is_delivery_crew(user):
      orders = Order.objects.all().filter(crew=user)

    elif is_customer(user):
      orders = Order.objects.all().filter(customer=user)

    customer = self.request.query_params.get('customer')
    if customer is not None:
      orders = orders.filter(customer=customer)

    crew = self.request.query_params.get('crew')
    if crew is not None:
      orders = orders.filter(crew=crew)

    status = self.request.query_params.get('status')
    if status is not None:
      orders = orders.filter(status=status)

    return orders

  def list(self, request, *args, **kwargs):
    return super().list(request, *args, **kwargs)

  def create(self, request):
    items_cart = Cart.objects.all().filter(user=request.user)
    if (len(items_cart) == 0):
      return JsonResponse({'detail': 'Empty Cart'}, status=status.HTTP_400_BAD_REQUEST)
    order = Order.objects.create(status=0, customer=request.user)
    for item_cart in items_cart:
      order_item = ItemOrder.objects.create(
        order=order, menu_item=item_cart.menu_item, quantity=item_cart.quantity
      )
      item_cart.delete()
      order_item.save()
    order.save()
    return JsonResponse(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

  def update(self, request, pk=None):
    order = get_object_or_404(Order, pk=pk)

    order_status = request.POST.get('status')
    crew_id = request.POST.get('crew_id')
    if order_status is None or crew_id is None:
      return JsonResponse({'detail': 'Missing element'}, status=status.HTTP_400_BAD_REQUEST)

    order.status = order_status

    user = get_object_or_404(User, pk=crew_id)
    if not is_delivery_crew(user):
      return JsonResponse({'detail': 'User is not from the delivery crew'}, status=status.HTTP_400_BAD_REQUEST)
    order.crew = user
    order.save()

    return JsonResponse(OrderSerializer(order).data, status=status.HTTP_200_OK)

  def partial_update(self, request, pk=None):
    order = get_object_or_404(Order, pk=pk)

    order_status = request.POST.get('status')
    crew_id = request.POST.get('crew_id')

    if order_status is not None:
      order.status = order_status

    if is_manager(request.user) and crew_id is not None:
      user = get_object_or_404(User, pk=crew_id)
      if not is_delivery_crew(user):
        return JsonResponse({'detail': 'User is not from the delivery crew'}, status=status.HTTP_400_BAD_REQUEST)
      order.crew = user

    order.save()

    return JsonResponse(OrderSerializer(order).data, status=status.HTTP_200_OK)
